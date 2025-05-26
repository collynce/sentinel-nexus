<template>
    <div class="space-y-6">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Settings</h1>
        <p class="text-muted-foreground">Manage your account and application preferences</p>
      </div>

      <Tabs defaultValue="general" class="w-full">
        <TabsList>
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="api">API Keys</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
        </TabsList>
        
        <!-- General Settings -->
        <TabsContent value="general" class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Profile</CardTitle>
              <CardDescription>Manage your personal information</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="space-y-2">
                  <Label for="name">Name</Label>
                  <Input id="name" value="Security Analyst" />
                </div>
                <div class="space-y-2">
                  <Label for="email">Email</Label>
                  <Input id="email" type="email" value="analyst@example.com" />
                </div>
              </div>
              <div class="space-y-2">
                <Label for="role">Role</Label>
                <Select defaultValue="analyst">
                  <SelectTrigger id="role">
                    <SelectValue placeholder="Select a role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="analyst">Security Analyst</SelectItem>
                    <SelectItem value="manager">SOC Manager</SelectItem>
                    <SelectItem value="admin">Administrator</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save Changes</Button>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Appearance</CardTitle>
              <CardDescription>Customize the application appearance</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div class="space-y-2">
                <Label>Theme</Label>
                <RadioGroup defaultValue="system">
                  <div class="flex items-center gap-4">
                    <div class="flex items-center space-x-2">
                      <RadioGroupItem value="light" id="light" />
                      <Label for="light">Light</Label>
                    </div>
                    <div class="flex items-center space-x-2">
                      <RadioGroupItem value="dark" id="dark" />
                      <Label for="dark">Dark</Label>
                    </div>
                    <div class="flex items-center space-x-2">
                      <RadioGroupItem value="system" id="system" />
                      <Label for="system">System</Label>
                    </div>
                  </div>
                </RadioGroup>
              </div>
              <div class="space-y-2">
                <Label>Dashboard Layout</Label>
                <Select defaultValue="default">
                  <SelectTrigger>
                    <SelectValue placeholder="Select layout" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="default">Default</SelectItem>
                    <SelectItem value="compact">Compact</SelectItem>
                    <SelectItem value="expanded">Expanded</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save Changes</Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <!-- Notifications Settings -->
        <TabsContent value="notifications" class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <CardDescription>Configure how you receive notifications</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div class="space-y-0.5">
                    <Label>Critical Threats</Label>
                    <p class="text-sm text-muted-foreground">Receive alerts for critical severity threats</p>
                  </div>
                  <Switch checked />
                </div>
                <Separator />
                <div class="flex items-center justify-between">
                  <div class="space-y-0.5">
                    <Label>High Severity Threats</Label>
                    <p class="text-sm text-muted-foreground">Receive alerts for high severity threats</p>
                  </div>
                  <Switch checked />
                </div>
                <Separator />
                <div class="flex items-center justify-between">
                  <div class="space-y-0.5">
                    <Label>Medium Severity Threats</Label>
                    <p class="text-sm text-muted-foreground">Receive alerts for medium severity threats</p>
                  </div>
                  <Switch />
                </div>
                <Separator />
                <div class="flex items-center justify-between">
                  <div class="space-y-0.5">
                    <Label>Low Severity Threats</Label>
                    <p class="text-sm text-muted-foreground">Receive alerts for low severity threats</p>
                  </div>
                  <Switch />
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save Changes</Button>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Delivery Methods</CardTitle>
              <CardDescription>Configure how notifications are delivered</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div class="space-y-0.5">
                    <Label>In-App Notifications</Label>
                    <p class="text-sm text-muted-foreground">Show notifications within the application</p>
                  </div>
                  <Switch checked />
                </div>
                <Separator />
                <div class="flex items-center justify-between">
                  <div class="space-y-0.5">
                    <Label>Email Notifications</Label>
                    <p class="text-sm text-muted-foreground">Send notifications to your email address</p>
                  </div>
                  <Switch checked />
                </div>
                <Separator />
                <div class="flex items-center justify-between">
                  <div class="space-y-0.5">
                    <Label>SMS Notifications</Label>
                    <p class="text-sm text-muted-foreground">Send notifications via SMS</p>
                  </div>
                  <Switch />
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save Changes</Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <!-- API Keys Settings -->
        <TabsContent value="api" class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>API Keys</CardTitle>
              <CardDescription>Manage your API keys for accessing the Sentinel Nexus API</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div class="space-y-4">
                <div class="rounded-md border p-4">
                  <div class="flex items-start justify-between">
                    <div>
                      <div class="flex items-center gap-2">
                        <h3 class="font-medium">Production API Key</h3>
                        <Badge>Active</Badge>
                      </div>
                      <p class="text-sm text-muted-foreground mt-1">Created on May 15, 2025</p>
                    </div>
                    <Button variant="outline" size="sm">
                      <Icon name="lucide:rotate-cw" class="mr-2 h-4 w-4" />
                      Rotate
                    </Button>
                  </div>
                  <div class="mt-4">
                    <div class="flex items-center gap-2">
                      <Input value="sk_prod_*****************************" readOnly />
                      <Button variant="ghost" size="icon">
                        <Icon name="lucide:copy" class="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
                <div class="rounded-md border p-4">
                  <div class="flex items-start justify-between">
                    <div>
                      <div class="flex items-center gap-2">
                        <h3 class="font-medium">Development API Key</h3>
                        <Badge variant="outline">Testing</Badge>
                      </div>
                      <p class="text-sm text-muted-foreground mt-1">Created on May 20, 2025</p>
                    </div>
                    <Button variant="outline" size="sm">
                      <Icon name="lucide:rotate-cw" class="mr-2 h-4 w-4" />
                      Rotate
                    </Button>
                  </div>
                  <div class="mt-4">
                    <div class="flex items-center gap-2">
                      <Input value="sk_dev_*****************************" readOnly />
                      <Button variant="ghost" size="icon">
                        <Icon name="lucide:copy" class="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Button>
                <Icon name="lucide:plus" class="mr-2 h-4 w-4" />
                Create New API Key
              </Button>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>API Usage</CardTitle>
              <CardDescription>Monitor your API usage and limits</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div class="space-y-4">
                <div>
                  <div class="flex items-center justify-between">
                    <Label>API Calls (This Month)</Label>
                    <span class="text-sm font-medium">12,458 / 50,000</span>
                  </div>
                  <div class="mt-2 h-2 w-full overflow-hidden rounded-full bg-muted">
                    <div class="h-full bg-primary" style="width: 25%"></div>
                  </div>
                  <p class="text-xs text-muted-foreground mt-1">25% of monthly limit used</p>
                </div>
                <Separator />
                <div>
                  <div class="flex items-center justify-between">
                    <Label>Rate Limit</Label>
                    <span class="text-sm font-medium">100 requests/minute</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <!-- Integrations Settings -->
        <TabsContent value="integrations" class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>External Integrations</CardTitle>
              <CardDescription>Connect Sentinel Nexus with external services</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <div class="bg-muted p-2 rounded-md">
                      <Icon name="lucide:slack" class="h-6 w-6" />
                    </div>
                    <div>
                      <h3 class="font-medium">Slack</h3>
                      <p class="text-sm text-muted-foreground">Send alerts and reports to Slack channels</p>
                    </div>
                  </div>
                  <Button variant="outline">
                    Connect
                  </Button>
                </div>
                <Separator />
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <div class="bg-muted p-2 rounded-md">
                      <Icon name="lucide:mail" class="h-6 w-6" />
                    </div>
                    <div>
                      <h3 class="font-medium">Microsoft Teams</h3>
                      <p class="text-sm text-muted-foreground">Share intelligence with your team</p>
                    </div>
                  </div>
                  <Button variant="outline">
                    Connect
                  </Button>
                </div>
                <Separator />
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <div class="bg-muted p-2 rounded-md">
                      <Icon name="lucide:shield" class="h-6 w-6" />
                    </div>
                    <div>
                      <h3 class="font-medium">SIEM Integration</h3>
                      <p class="text-sm text-muted-foreground">Connect with your SIEM solution</p>
                    </div>
                  </div>
                  <Button variant="outline">
                    Connect
                  </Button>
                </div>
                <Separator />
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <div class="bg-muted p-2 rounded-md">
                      <Icon name="lucide:webhook" class="h-6 w-6" />
                    </div>
                    <div>
                      <h3 class="font-medium">Webhooks</h3>
                      <p class="text-sm text-muted-foreground">Send data to custom endpoints</p>
                    </div>
                  </div>
                  <Button variant="outline">
                    Configure
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Switch } from '@/components/ui/switch'
import { Separator } from '@/components/ui/separator'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
</script>
