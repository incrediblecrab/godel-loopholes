/**
 * Chart geometry, computed at build time.
 *
 * WHY D3 AND NOT A CHART LIBRARY. A charting library ships a renderer, a theme
 * and a toolbar, and the theme is the part you can see. Every such library has
 * a house style, and a reader who has seen one chart in that style has seen the
 * house style rather than this argument. D3 is not a charting library: it is
 * scales, shapes and interpolators, and it draws nothing on its own. What gets
 * drawn is in this repository, which is the point.
 *
 * WHY BUILD TIME. These functions run in Astro frontmatter, so the SVG they
 * describe is computed during `astro build` and served as markup. Three
 * consequences, all of them load-bearing here:
 *
 *   - The charts are in the HTML, so they render with scripting disabled. The
 *     browser suite asserts this, and a chart that vanished without JavaScript
 *     would fail a document whose entire value is that it can be checked.
 *   - No D3 reaches the client. The bytes stay in node_modules.
 *   - The geometry is computed once, by the build, from data/facts.json --
 *     rather than recomputed in every reader's browser from numbers typed into
 *     a script, which is a second source of truth wearing a disguise.
 *
 * Interaction is layered on top of static SVG rather than replacing it: where a
 * reader can change something, every state is precomputed here and the island
 * switches between them. That is why nothing in this file imports d3-selection.
 */
import { scaleLinear } from 'd3-scale';
import { format } from 'd3-format';

/** Thousands separators. `435` stays `435`; a five-figure count gets a comma. */
export const comma = format(',');

/**
 * The SVG user-space width every chart is laid out in. The rendered element is
 * responsive via a viewBox, so this number is a coordinate system rather than a
 * size in pixels: it never appears in the page and nothing depends on the
 * viewport matching it.
 */
export const CHART_W = 1000;

export interface Tick {
  /** Position along the value axis, in user space. */
  x: number;
  /** The value at that position, formatted for display. */
  label: string;
  /** Whether this tick sits at the very start or end of the domain. */
  terminal: boolean;
}

export interface ThresholdBarSpec {
  /** Total width of the drawn track, in user space. */
  width: number;
  /** Width of the filled portion, in user space. */
  fill: number;
  /** Position of the threshold marker, in user space. */
  marker: number;
  /** The share of the chamber the threshold represents, 0-1. */
  fraction: number;
  /** The share as a whole-number percentage, for display. */
  percent: number;
  /** Axis ticks, always including both ends of the domain. */
  ticks: Tick[];
}

/**
 * Geometry for one horizontal threshold bar: how many members of a chamber of
 * `size` are needed to reach `value`.
 *
 * The domain always starts at zero. A bar chart whose axis starts elsewhere
 * misrepresents the ratio it exists to show, and the ratio is the argument
 * here -- that a third of a chamber can propose an amendment.
 */
export function thresholdBar(value: number, size: number, tickCount = 4): ThresholdBarSpec {
  if (!Number.isFinite(value) || !Number.isFinite(size)) {
    throw new Error(`thresholdBar: value and size must be finite, got ${value} and ${size}`);
  }
  if (size <= 0) throw new Error(`thresholdBar: size must be positive, got ${size}`);
  if (value < 0 || value > size) {
    throw new Error(`thresholdBar: value ${value} is outside the chamber size ${size}`);
  }

  const x = scaleLinear().domain([0, size]).range([0, CHART_W]);

  // d3's tick algorithm chooses round numbers and may omit the domain maximum,
  // which for a chamber size is the one tick a reader most needs -- it is what
  // the bar is a fraction OF. So the ends are added and any tick close enough
  // to collide with them is dropped. The gap is 12%: at 8% a chamber of 435
  // kept a tick at 400, which sits eighty user-space units from the 435 label
  // and overprints it at any real rendered width.
  const raw = x.ticks(tickCount).filter((t) => t > 0 && t < size);
  const minGap = size * 0.12;
  const interior = raw.filter((t) => t > minGap && t < size - minGap);

  const ticks: Tick[] = [
    { x: 0, label: '0', terminal: true },
    ...interior.map((t) => ({ x: x(t), label: comma(t), terminal: false })),
    { x: CHART_W, label: comma(size), terminal: true },
  ];

  const fraction = value / size;

  return {
    width: CHART_W,
    fill: x(value),
    marker: x(value),
    fraction,
    percent: Math.round(fraction * 100),
    ticks,
  };
}
