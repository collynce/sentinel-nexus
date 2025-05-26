from typing import List, Optional, Dict, Any
import uuid
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import litellm
from loguru import logger

from app.models.analysis import Analysis, AnalysisStatus
from app.schemas.analysis import AnalysisCreate, AnalysisResult
from app.core.config import settings

class AnalysisService:
    """Service for AI-powered threat analysis"""
    
    def __init__(self, db: AsyncSession):
        """Initialize with database session"""
        self.db = db
        
        # Configure LiteLLM
        litellm.api_key = settings.OPENROUTER_API_KEY
        litellm.set_verbose = True
        

    
    async def get_analysis_results(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
    ) -> List[Analysis]:
        """Get list of analysis results with optional filtering"""
        query = select(Analysis).offset(skip).limit(limit)
        
        # Apply filters if provided
        if status:
            query = query.filter(Analysis.status == status)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_analysis_result(self, analysis_id: str) -> Optional[Analysis]:
        """Get a specific analysis result by ID"""
        query = select(Analysis).filter(Analysis.id == analysis_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def analyze_content(self, analysis_data: AnalysisCreate) -> AnalysisResult:
        """Submit content for threat analysis (manual or API-triggered)"""
        # Analyze the content using the modular threat_analysis_agent
        from app.agents.threat_analysis.agent import root_agent as threat_analysis_agent
        analysis_result = await threat_analysis_agent.run(analysis_data.content)

        # Create a new analysis record
        db_analysis = Analysis(
            content=analysis_data.content,
            analysis_type=analysis_data.analysis_type,
            content_id=analysis_data.content_id,
            status=AnalysisStatus.PENDING,
            model_parameters=analysis_data.model_parameters,
            results=analysis_result,
        )
        self.db.add(db_analysis)
        await self.db.commit()
        await self.db.refresh(db_analysis)
        db_analysis.status = AnalysisStatus.COMPLETED
        await self.db.commit()
        return analysis_result

    async def run_autonomous_threat_intel(self, objectives: list[str]):
        """
        Run the autonomous end-to-end pipeline for a list of objectives.
        For each objective:
            1. Run data collection pipeline
            2. Pass output to threat analysis pipeline
            3. Store both results in the database
        """
        from app.agents.threat_analysis.agent import root_agent as data_collection_pipeline
        from app.agents.threat_analysis.agent import root_agent as threat_analysis_agent
        results = []
        for objective in objectives:
            try:
                # Step 1: Data Collection
                data_result = await data_collection_pipeline.run(objective)
                content = data_result.get("synthesized_intel") or data_result.get("collected_data")
                if not content:
                    continue
                # Step 2: Threat Analysis
                analysis_result = await threat_analysis_agent.run(content)
                # Step 3: Store in DB
                db_analysis = Analysis(
                    content=content,
                    analysis_type="autonomous",
                    content_id=None,
                    status=AnalysisStatus.COMPLETED,
                    model_parameters=None,
                    results=analysis_result,
                )
                self.db.add(db_analysis)
                await self.db.commit()
                await self.db.refresh(db_analysis)
                results.append({
                    "objective": objective,
                    "data_collection": data_result,
                    "threat_analysis": analysis_result,
                    "db_id": db_analysis.id
                })
            except Exception as e:
                results.append({"objective": objective, "error": str(e)})
        return results

        await self.db.commit()
        await self.db.refresh(db_analysis)

        return AnalysisResult(
            analysis_id=db_analysis.id,
            status=AnalysisStatus.COMPLETED,
            message="Analysis completed successfully",
        )
    
    async def extract_iocs(self, text: str) -> Dict[str, Any]:
        """Extract Indicators of Compromise from text using LLM"""
        try:
            # Define the prompt for IOC extraction
            prompt = f"""
            Extract all potential Indicators of Compromise (IOCs) from the following text.
            Return the results as a JSON object with the following structure:
            {{
                "ip_addresses": [
                    {{"value": "1.2.3.4", "confidence": 0.95}}
                ],
                "domains": [
                    {{"value": "example.com", "confidence": 0.92}}
                ],
                "urls": [
                    {{"value": "https://malicious.com/path", "confidence": 0.88}}
                ],
                "hashes": [
                    {{"type": "md5", "value": "d41d8cd98f00b204e9800998ecf8427e", "confidence": 0.97}}
                ],
                "emails": [
                    {{"value": "phish@example.com", "confidence": 0.91}}
                ]
            }}
            
            Only include items that are likely to be actual IOCs. For each IOC, provide a confidence score between 0 and 1.
            
            Text to analyze:
            {text}
            """
            
            # Call the LLM using LiteLLM
            response = await litellm.acompletion(
                model=settings.DEFAULT_LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1500,
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Extract the JSON part
            try:
                # Try to parse the entire content as JSON
                iocs = json.loads(content)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the text
                import re
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    iocs = json.loads(json_match.group(1))
                else:
                    # If still no JSON, return empty results
                    iocs = {
                        "ip_addresses": [],
                        "domains": [],
                        "urls": [],
                        "hashes": [],
                        "emails": []
                    }
            
            return iocs
        except Exception as e:
            logger.error(f"Error extracting IOCs: {str(e)}")
            return {
                "error": str(e),
                "ip_addresses": [],
                "domains": [],
                "urls": [],
                "hashes": [],
                "emails": []
            }
    
    async def assess_risk(self, content: str, iocs: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the risk level of content and IOCs using LLM"""
        try:
            # Define the prompt for risk assessment
            prompt = f"""
            Assess the risk level of the following threat intelligence content and extracted IOCs.
            Return the results as a JSON object with the following structure:
            {{
                "overall_risk_score": 0.85,
                "risk_level": "high",
                "confidence": 0.92,
                "reasoning": "This appears to be a sophisticated phishing campaign targeting financial institutions...",
                "recommended_actions": [
                    "Block all identified IP addresses",
                    "Monitor for additional indicators"
                ]
            }}
            
            Content:
            {content}
            
            Extracted IOCs:
            {json.dumps(iocs, indent=2)}
            """
            
            # Call the LLM using LiteLLM
            response = await litellm.acompletion(
                model=settings.DEFAULT_LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1000,
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Extract the JSON part
            try:
                # Try to parse the entire content as JSON
                risk_assessment = json.loads(content)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the text
                import re
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    risk_assessment = json.loads(json_match.group(1))
                else:
                    # If still no JSON, return a default assessment
                    risk_assessment = {
                        "overall_risk_score": 0.5,
                        "risk_level": "medium",
                        "confidence": 0.7,
                        "reasoning": "Unable to properly assess risk from the provided content.",
                        "recommended_actions": ["Manual review required"]
                    }
            
            return risk_assessment
        except Exception as e:
            logger.error(f"Error assessing risk: {str(e)}")
            return {
                "error": str(e),
                "overall_risk_score": 0.5,
                "risk_level": "unknown",
                "confidence": 0.0,
                "reasoning": f"Error during risk assessment: {str(e)}",
                "recommended_actions": ["Manual review required"]
            }
