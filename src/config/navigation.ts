import { Bot, BookOpen, Code2, GitCompare, Layers3, Network, RadioTower, Workflow, type LucideIcon } from "lucide-react";

type NavigationItem = {
  key: string;
  path: string;
  icon?: LucideIcon;
  isContentType?: boolean;
};

export const NAVIGATION_CONFIG: NavigationItem[] = [
  { key: "guide", path: "/guide", icon: BookOpen, isContentType: true },
  { key: "model", path: "/model", icon: Bot, isContentType: true },
  { key: "api", path: "/api", icon: Code2, isContentType: true },
  { key: "typesafe", path: "/typesafe", icon: Layers3, isContentType: true },
  { key: "agent", path: "/agent", icon: Workflow, isContentType: true },
  { key: "integrations", path: "/integrations", icon: Network, isContentType: true },
  { key: "comparisons", path: "/comparisons", icon: GitCompare, isContentType: true },
  { key: "community", path: "/community", icon: RadioTower, isContentType: true },
];

export const CONTENT_TYPES = NAVIGATION_CONFIG.filter((item) => item.isContentType).map((item) => item.path.replace(/^\//, ""));
