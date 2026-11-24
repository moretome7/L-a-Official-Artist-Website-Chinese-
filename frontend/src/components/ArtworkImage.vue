<script setup lang="ts">
import { computed } from "vue";
import type { Artwork } from "../types";

const props = withDefaults(
  defineProps<{
    artwork: Artwork;
    eager?: boolean;
    compact?: boolean;
  }>(),
  {
    eager: false,
    compact: false,
  },
);

const label = computed(() => {
  if (props.artwork.series === "moon") return "MOON PHASE";
  if (props.artwork.series === "nebula") return "NEBULA STUDY";
  if (props.artwork.series === "deep") return "DEEP FIELD";
  return "PLANETARY STUDY";
});

const artworkUrl = computed(() => {
  const params = new URLSearchParams({
    title: props.artwork.title,
    tone: props.artwork.tone,
    series: props.artwork.series,
    label: label.value,
  });
  return `data:image/svg+xml,${encodeURIComponent(renderSvg(params))}`;
});

function renderSvg(params: URLSearchParams): string {
  const title = escapeXml(params.get("title") ?? "").slice(0, 30);
  const tone = params.get("tone") ?? "mist";
  const series = params.get("series") ?? "planet";
  const label = escapeXml(params.get("label") ?? "");
  const palettes: Record<string, [string, string, string, string, string]> = {
    mist: ["#e9ece8", "#b7c6d0", "#9cafbb", "#d8c8ab", "#3f4951"],
    mauve: ["#eee9e4", "#c9c2d8", "#a7a0b8", "#d9c6ae", "#514b5d"],
    gold: ["#f0ebe0", "#d6c6a3", "#bea778", "#b8c5c7", "#514c40"],
    slate: ["#e4e7e6", "#aebdca", "#788999", "#c6b89f", "#35404a"],
  };
  const [base, blue, blueDeep, gold, ink] = palettes[tone] ?? palettes.mist;
  const celestial =
    series === "moon"
      ? `<circle cx="258" cy="292" r="112" fill="${gold}" opacity=".82"/><path d="M258 180a112 112 0 0 1 0 224 126 126 0 0 1 0-224Z" fill="${ink}" opacity=".22"/>`
      : series === "deep"
        ? `<ellipse cx="270" cy="336" rx="190" ry="82" fill="${ink}" opacity=".15"/><circle cx="158" cy="254" r="4" fill="${gold}"/><circle cx="393" cy="206" r="3" fill="${blueDeep}"/><circle cx="322" cy="417" r="3" fill="${gold}" opacity=".9"/>`
        : series === "nebula"
          ? `<ellipse cx="265" cy="304" rx="177" ry="137" fill="${blue}" opacity=".72"/><ellipse cx="321" cy="280" rx="119" ry="163" fill="${gold}" opacity=".48" transform="rotate(28 321 280)"/><ellipse cx="215" cy="335" rx="143" ry="92" fill="${blueDeep}" opacity=".38" transform="rotate(-23 215 335)"/>`
          : `<circle cx="264" cy="302" r="137" fill="${blue}"/><ellipse cx="264" cy="302" rx="216" ry="53" fill="none" stroke="${gold}" stroke-width="9" opacity=".62" transform="rotate(-16 264 302)"/><ellipse cx="264" cy="302" rx="198" ry="41" fill="none" stroke="${ink}" stroke-width="1.3" opacity=".42" transform="rotate(-16 264 302)"/>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 700"><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="${base}"/><stop offset="1" stop-color="${blue}" stop-opacity=".3"/></linearGradient><radialGradient id="glow"><stop stop-color="${gold}" stop-opacity=".64"/><stop offset="1" stop-color="${gold}" stop-opacity="0"/></radialGradient><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".82" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .11"/></feComponentTransfer></filter></defs><rect width="560" height="700" fill="url(#bg)"/><circle cx="92" cy="108" r="126" fill="url(#glow)"/><path d="M-25 580C105 504 201 548 306 489c101-58 163-37 281 22v189H-25Z" fill="${base}" opacity=".64"/><g>${celestial}</g><g fill="${ink}" opacity=".32"><circle cx="88" cy="242" r="2.2"/><circle cx="445" cy="124" r="1.8"/><circle cx="478" cy="468" r="2.4"/><circle cx="109" cy="481" r="1.4"/><circle cx="401" cy="559" r="1.6"/></g><rect width="560" height="700" filter="url(#grain)" opacity=".8"/><path d="M38 58h70M38 58v70M522 642h-70M522 642v-70" fill="none" stroke="${ink}" stroke-width="1" opacity=".34"/><text x="44" y="627" fill="${ink}" fill-opacity=".55" font-family="Georgia,serif" font-size="11" letter-spacing="2.3">${label}</text><text x="44" y="650" fill="${ink}" fill-opacity=".72" font-family="Georgia,serif" font-size="18" font-style="italic">${title}</text></svg>`;
}

function escapeXml(value: string): string {
  return value.replace(/[<>&"']/g, (character) => {
    const entities: Record<string, string> = {
      "<": "&lt;",
      ">": "&gt;",
      "&": "&amp;",
      '"': "&quot;",
      "'": "&apos;",
    };
    return entities[character] ?? character;
  });
}
</script>

<template>
  <div class="artwork-image" :class="{ 'artwork-image--compact': compact }">
    <img
      :src="artworkUrl"
      :alt="`《${artwork.title}》，${artwork.year} 年，${artwork.medium}`"
      :loading="eager ? 'eager' : 'lazy'"
      decoding="async"
    />
  </div>
</template>