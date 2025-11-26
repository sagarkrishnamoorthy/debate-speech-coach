// Type declaration overrides for React 19 compatibility
declare module 'recharts' {
  import { ComponentType } from 'react';
  
  export const ResponsiveContainer: ComponentType<any>;
  export const RadarChart: ComponentType<any>;
  export const PolarGrid: ComponentType<any>;
  export const PolarAngleAxis: ComponentType<any>;
  export const PolarRadiusAxis: ComponentType<any>;
  export const Radar: ComponentType<any>;
}
