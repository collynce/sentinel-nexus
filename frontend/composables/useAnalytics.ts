import { ref, onMounted, onUnmounted, markRaw } from "vue";
import { toast } from "vue-sonner";
import { useBackendApi } from "./useBackendApi";
import type { AxiosError } from "axios"; // Import AxiosError type for better error handling
// Define the Threat interface based on the backend schema
interface Threat {
  id: string;
  title: string;
  description?: string;
  severity: "critical" | "high" | "medium" | "low" | "info";
  threat_type?: string;
  created_at?: string;
  updated_at?: string;
  metadata?: {
    geo_ip?: {
      latitude?: string;
      longitude?: string;
      country_name?: string;
    };
    [key: string]: any;
  };
  [key: string]: any;
}

export interface AnalyticsFilters {
  severity?: string;
  type?: string;
  source?: string;
  status?: string;
  dateRange: {
    from: Date;
    to: Date;
  };
}

export interface AnalyticsStats {
  totalThreats: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  info: number;
  inProgress: number;
  resolved: number;
  newThreats: number;
}

export interface SeverityData {
  name: string;
  value: number;
  color: string;
}

export interface TrendData {
  date: string;
  value: number;
  severity: string;
}

export interface GeoData {
  name: string;
  value: [number, number, number];
}

export interface TypeData {
  name: string;
  value: number;
  color: string;
}

// Define API response interfaces
interface StatsResponse {
  total?: number;
  by_severity?: {
    critical?: number;
    high?: number;
    medium?: number;
    low?: number;
    info?: number;
  };
  by_status?: {
    in_progress?: number;
    resolved?: number;
  };
  new_last_24h?: number;
}

export function useAnalytics() {
  const api = useBackendApi();
  const loading = ref(false);
  const error = ref<string | null>(null);
  const lastUpdated = ref<Date | null>(null);
  let abortController: AbortController | null = null;

  // Default filters
  const filters = ref<AnalyticsFilters>({
    severity: "all",
    type: "all",
    source: "all",
    status: "all",
    dateRange: {
      from: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 7 days ago
      to: new Date(),
    },
  });

  // Stats
  const stats = ref<AnalyticsStats>({
    totalThreats: 0,
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
    info: 0,
    inProgress: 0,
    resolved: 0,
    newThreats: 0,
  });

  const severityData = ref<SeverityData[]>([]);
  const trendData = ref<TrendData[]>([]);
  const geoData = ref<GeoData[]>([]);
  const typeData = ref<TypeData[]>([]);
  const recentThreats = ref<Threat[]>([]);

  // Fetch all analytics data
  // Cancel any pending requests
  const cancelPendingRequest = () => {
    if (abortController) {
      abortController.abort();
      abortController = null;
    }
  };

  const fetchAnalyticsData = async () => {
    // Cancel any pending requests
    cancelPendingRequest();
    abortController = new AbortController();

    loading.value = true;
    error.value = null;

    try {
      // Validate date range
      if (filters.value.dateRange.from > filters.value.dateRange.to) {
        throw new Error(
          "Invalid date range: Start date must be before end date"
        );
      }

      // Update last updated timestamp
      lastUpdated.value = new Date();

      // Build query parameters from filters
      const params = {
        start_date: filters.value.dateRange.from.toISOString(),
        end_date: filters.value.dateRange.to.toISOString(),
        ...(filters.value.severity !== "all" && {
          severity: filters.value.severity,
        }),
        ...(filters.value.type !== "all" && { type: filters.value.type }),
        ...(filters.value.status !== "all" && { status: filters.value.status }),
      };

      // Fetch threats data with cancellation support
      const [threatsResponse, statsResponse] = await Promise.all([
        api.threats.getAll({
          ...params,
          signal: abortController?.signal,
        }) as Promise<Threat[]>,
        api.threats.getAll({
          ...params,
          stats: true,
          signal: abortController?.signal,
        }) as Promise<StatsResponse>,
      ]);

      // Process stats
      const threats = Array.isArray(threatsResponse) ? threatsResponse : [];
      const statsData = statsResponse || {};

      // Update stats
      stats.value = {
        totalThreats: statsData.total || 0,
        critical: statsData.by_severity?.critical || 0,
        high: statsData.by_severity?.high || 0,
        medium: statsData.by_severity?.medium || 0,
        low: statsData.by_severity?.low || 0,
        info: statsData.by_severity?.info || 0,
        inProgress: statsData.by_status?.in_progress || 0,
        resolved: statsData.by_status?.resolved || 0,
        newThreats: statsData.new_last_24h || 0,
      };

      // Process severity data
      severityData.value = [
        { name: "Critical", value: stats.value.critical, color: "#ef4444" },
        { name: "High", value: stats.value.high, color: "#f97316" },
        { name: "Medium", value: stats.value.medium, color: "#eab308" },
        { name: "Low", value: stats.value.low, color: "#3b82f6" },
        { name: "Info", value: stats.value.info, color: "#94a3b8" },
      ];

      // Process trend data (last 30 days)
      const now = new Date();
      const trendMap = new Map<
        string,
        { date: string; value: number; severity: string }
      >();

      // Initialize trend map with all dates
      for (let i = 29; i >= 0; i--) {
        const date = new Date(now);
        date.setDate(now.getDate() - i);
        const dateStr = date.toISOString().split("T")[0];
        trendMap.set(dateStr, { date: dateStr, value: 0, severity: "low" });
      }

      // Count threats by date
      threats.forEach((threat) => {
        if (threat.created_at) {
          const date = new Date(threat.created_at).toISOString().split("T")[0];
          const existing = trendMap.get(date);
          if (existing) {
            existing.value += 1;
            // Update severity to highest seen for the day
            const severities = ["info", "low", "medium", "high", "critical"];
            const currentSev = severities.indexOf(existing.severity);
            const threatSev = severities.indexOf(
              threat.severity?.toLowerCase() || "info"
            );
            if (threatSev > currentSev) {
              existing.severity = severities[threatSev];
            }
          }
        }
      });

      trendData.value = Array.from(trendMap.values());

      // Process geo data from threat metadata
      geoData.value = threats
        .filter(
          (
            t
          ): t is Threat & {
            metadata: {
              geo_ip: {
                latitude: string;
                longitude: string;
                country_name?: string;
              };
            };
          } => {
            // Validate geo data exists and has valid coordinates
            if (
              !t.metadata?.geo_ip?.latitude ||
              !t.metadata?.geo_ip?.longitude
            ) {
              return false;
            }
            const lat = parseFloat(t.metadata.geo_ip.latitude);
            const lng = parseFloat(t.metadata.geo_ip.longitude);
            return (
              !isNaN(lat) &&
              !isNaN(lng) &&
              lat >= -90 &&
              lat <= 90 &&
              lng >= -180 &&
              lng <= 180
            );
          }
        )
        .map((t) => {
          const lat = parseFloat(t.metadata.geo_ip.latitude);
          const lng = parseFloat(t.metadata.geo_ip.longitude);
          return {
            name: t.metadata.geo_ip.country_name || "Unknown",
            value: [lng, lat, 1] as [number, number, number], // [longitude, latitude, count]
          };
        })
        .reduce<Array<{ name: string; value: [number, number, number] }>>(
          (acc, curr) => {
            const existing = acc.find((g) => g.name === curr.name);
            if (existing) {
              existing.value[2] += 1; // Increment count for existing country
            } else {
              acc.push(curr);
            }
            return acc;
          },
          []
        );

      // Process type data
      const typeCounts = threats.reduce((acc, threat) => {
        const type = threat.threat_type || "Other";
        acc[type] = (acc[type] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);

      const colors = [
        "#ef4444",
        "#f97316",
        "#eab308",
        "#3b82f6",
        "#8b5cf6",
        "#ec4899",
      ];
      typeData.value = Object.entries(typeCounts).map(
        ([name, value], index) => ({
          name,
          value,
          color: colors[index % colors.length] || "#94a3b8",
        })
      );

      // Store recent threats
      recentThreats.value = threats.slice(0, 10);

      // Show success toast with markRaw to prevent reactivity
      const successOptions = markRaw({
        description: `Last updated: ${new Date().toLocaleString()}`,
        action: markRaw({
          label: 'Dismiss',
          onClick: () => {}
        })
      });
      toast.success('Analytics data updated', successOptions);

      return {
        stats: stats.value,
        severityData: severityData.value,
        trendData: trendData.value,
        geoData: geoData.value,
        typeData: typeData.value,
        recentThreats: recentThreats.value,
      };
    } catch (err) {
      // Don't show error if request was aborted
      if ((err as Error).name === 'AbortError') {
        return
      }
      
      console.error('Error fetching analytics data:', err)
      
      // Handle Axios errors
      const errorMessage = (err as AxiosError).response?.data?.message || 
                         (err as Error).message || 
                         'Failed to load analytics data'
      
      error.value = errorMessage
      
      // Show error toast with retry action and markRaw
      const errorOptions = markRaw({
        description: errorMessage,
        action: markRaw({
          label: 'Retry',
          onClick: () => fetchAnalyticsData()
        })
      });
      toast.error('Error loading analytics data', errorOptions);
      throw err;
    } finally {
      loading.value = false;
      // Clean up the abort controller
      if (abortController) {
        abortController = null;
      }
    }
  };

  // Watch for filter changes with debounce
  let filterTimeout: NodeJS.Timeout | null = null;

  const handleFilterChange = () => {
    // Cancel any pending request and timeout
    cancelPendingRequest();
    if (filterTimeout) {
      clearTimeout(filterTimeout);
    }

    // Set a new timeout
    filterTimeout = setTimeout(() => {
      fetchAnalyticsData().catch(() => {
        // Error is already handled in fetchAnalyticsData
      });
    }, 300);
  };

  // Cleanup on unmount
  onUnmounted(() => {
    // Cancel any pending requests and timeouts
    cancelPendingRequest();
    if (filterTimeout) {
      clearTimeout(filterTimeout);
      filterTimeout = null;
    }
  });

  // Initialize data
  onMounted(() => {
    fetchAnalyticsData().catch(() => {
      // Error is already handled in fetchAnalyticsData
    });
  });

  return {
    loading,
    error,
    lastUpdated,
    filters,
    stats,
    severityData,
    trendData,
    geoData,
    typeData,
    recentThreats,
    fetchAnalyticsData,
    handleFilterChange,
  };
}
