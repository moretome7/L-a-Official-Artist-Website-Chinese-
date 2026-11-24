export type RouteName = "home" | "works" | "about" | "commission" | "contact";

export type SeriesId = "planet" | "nebula" | "moon" | "deep";

export type Medium = "油画" | "丙烯" | "数字绘画" | "纸本";

export type ArtworkStatus = "可收藏" | "已售出" | "仅展示" | "限量版画在售";

export type ArtworkTone = "mist" | "mauve" | "gold" | "slate";

export interface NavigationOptions {
  hash?: string;
  workTitle?: string;
  commissionType?: string;
}

export interface Artwork {
  id: string;
  title: string;
  year: number;
  medium: Medium;
  dimensions: string;
  series: SeriesId;
  status: ArtworkStatus;
  tone: ArtworkTone;
  note: string;
  edition?: string;
}

export interface SeriesOption {
  id: SeriesId;
  name: string;
  english: string;
  description: string;
}