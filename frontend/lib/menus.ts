import type { NavMenu, NavMenuItems } from "~/types/nav";

export const navMenu: NavMenu[] = [
  {
    heading: "Overview",
    items: [
      {
        title: "Dashboard",
        icon: "i-lucide-layout-dashboard",
        link: "/dashboard",
      },
      {
        title: "Analytics",
        icon: "i-lucide-bar-chart-2",
        link: "/analytics",
      },
    ],
  },
  {
    heading: "Threat Intelligence",
    items: [
      {
        title: "Threats",
        icon: "i-lucide-shield-alert",
        link: "/threats",
      },
      {
        title: "Sources",
        icon: "i-lucide-database",
        link: "/sources",
      },
      {
        title: "Reports",
        icon: "i-lucide-file-text",
        link: "/reports",
      },
      {
        title: "Indicators",
        icon: "i-lucide-target",
        link: "/indicators",
      },
    ],
  },
  {
    heading: "Operations",
    items: [
      {
        title: "Incidents",
        icon: "i-lucide-alert-triangle",
        link: "/incidents",
      },
      {
        title: "Alerts",
        icon: "i-lucide-bell",
        link: "/alerts",
        badge: {
          content: "5",
          color: "red",
        },
      },
      {
        title: "SOC Co-Pilot",
        icon: "i-lucide-message-square",
        link: "/copilot",
        new: true,
      },
    ],
  },
  {
    heading: "Administration",
    items: [
      {
        title: "Settings",
        icon: "i-lucide-settings",
        children: [
          {
            title: "General",
            icon: "i-lucide-circle",
            link: "/settings/general",
          },
          {
            title: "Integrations",
            icon: "i-lucide-plug",
            link: "/integrations",
          },
          {
            title: "API Documentation",
            icon: "i-lucide-file-code",
            link: "/api-docs",
          },
          {
            title: "Tools",
            icon: "i-lucide-wrench",
            children: [
              {
                title: "Threat Scanner",
                icon: "i-lucide-scan",
                link: "/tools/threat-scanner",
              },
              {
                title: "IOC Analyzer",
                icon: "i-lucide-search",
                link: "/tools/ioc-analyzer",
              },
              {
                title: "Malware Sandbox",
                icon: "i-lucide-box",
                link: "/tools/malware-sandbox",
              },
              {
                title: "PCAP Analyzer",
                icon: "i-lucide-activity",
                link: "/tools/pcap-analyzer",
              },
              {
                title: "Vulnerability Scanner",
                icon: "i-lucide-shield",
                link: "/tools/vulnerability-scanner",
              },
            ],
          },
          {
            title: "Users",
            icon: "i-lucide-circle",
            link: "/settings/users",
          },
          {
            title: "API Keys",
            icon: "i-lucide-circle",
            link: "/settings/api-keys",
          },
        ],
      },
    ],
  },
];

export const navMenuBottom: NavMenuItems[] = [];

export const userNavItems: NavMenuItems[] = [
  {
    title: "Profile",
    icon: "i-lucide-user",
    link: "/profile",
  },
  {
    title: "Settings",
    icon: "i-lucide-settings",
    link: "/settings",
  },
  {
    title: "Logout",
    icon: "i-lucide-log-out",
    link: "/logout",
  },
];
