<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import ArtworkImage from "../components/ArtworkImage.vue";
import { getSeries, seriesOptions, works } from "../data/works";
import type { ArtworkStatus, Medium, RouteName, SeriesId } from "../types";

const props = withDefaults(
  defineProps<{
    initialSeries?: SeriesId | "all";
    initialWorkId?: string;
  }>(),
  {
    initialSeries: "all",
    initialWorkId: "",
  },
);

const emit = defineEmits<{
  navigate: [name: RouteName];
  consult: [workTitle: string];
}>();

const mediaOptions: Array<Medium | "all"> = ["all", "油画", "丙烯", "数字绘画", "纸本"];
const activeSeries = ref<SeriesId | "all">(props.initialSeries);
const activeMedium = ref<Medium | "all">("all");
const modalIndex = ref(-1);
const modalOpen = computed(() => modalIndex.value >= 0);
const closeButton = ref<HTMLButtonElement | null>(null);
let previousFocus: HTMLElement | null = null;
let isApplyingContext = false;

const filteredWorks = computed(() =>
  works.filter((artwork) => {
    const seriesMatches = activeSeries.value === "all" || artwork.series === activeSeries.value;
    const mediumMatches = activeMedium.value === "all" || artwork.medium === activeMedium.value;
    return seriesMatches && mediumMatches;
  }),
);

const currentSeries = computed(() => getSeries(activeSeries.value));
const currentArtwork = computed(() => filteredWorks.value[modalIndex.value]);
const resultSummary = computed(() => `${filteredWorks.value.length} 件作品`);
const hasFilters = computed(() => activeSeries.value !== "all" || activeMedium.value !== "all");

watch(
  () => [props.initialSeries, props.initialWorkId] as const,
  ([series, workId]) => {
    isApplyingContext = true;
    const targetWork = workId ? works.find((artwork) => artwork.id === workId) : undefined;

    activeMedium.value = "all";
    activeSeries.value = targetWork?.series ?? series;

    nextTick(() => {
      if (targetWork) openPreview(targetWork.id);
      else closePreview();
      isApplyingContext = false;
    });
  },
  { immediate: true },
);

watch([activeSeries, activeMedium], () => {
  if (isApplyingContext) return;
  closePreview();
});

function statusClass(status: ArtworkStatus) {
  return {
    "status-pill--available": status === "可收藏",
    "status-pill--sold": status === "已售出",
    "status-pill--display": status === "仅展示",
    "status-pill--edition": status === "限量版画在售",
  };
}

function selectSeries(series: SeriesId | "all"): void {
  activeSeries.value = series;
}

function openPreview(workId: string): void {
  const index = filteredWorks.value.findIndex((artwork) => artwork.id === workId);
  if (index < 0) return;
  previousFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
  modalIndex.value = index;
  document.body.style.overflow = "hidden";
  nextTick(() => closeButton.value?.focus());
}

function closePreview(): void {
  modalIndex.value = -1;
  document.body.style.overflow = "";
  if (previousFocus) {
    const focusTarget = previousFocus;
    previousFocus = null;
    nextTick(() => focusTarget.focus());
  }
}

function showPrevious(): void {
  const total = filteredWorks.value.length;
  if (!total) return;
  modalIndex.value = (modalIndex.value - 1 + total) % total;
}

function showNext(): void {
  const total = filteredWorks.value.length;
  if (!total) return;
  modalIndex.value = (modalIndex.value + 1) % total;
}

function resetFilters(): void {
  activeSeries.value = "all";
  activeMedium.value = "all";
}

function requestCommission(workTitle: string): void {
  closePreview();
  emit("consult", workTitle);
}

function onKeydown(event: KeyboardEvent): void {
  if (!modalOpen.value) return;
  if (event.key === "Escape") {
    event.preventDefault();
    closePreview();
  }
  if (event.key === "ArrowLeft") {
    event.preventDefault();
    showPrevious();
  }
  if (event.key === "ArrowRight") {
    event.preventDefault();
    showNext();
  }
}

onMounted(() => window.addEventListener("keydown", onKeydown));
onBeforeUnmount(() => {
  window.removeEventListener("keydown", onKeydown);
  document.body.style.overflow = "";
});
</script>

<template>
  <main>
    <section class="works-hero page-shell" aria-labelledby="works-title">
      <nav class="breadcrumb" aria-label="面包屑导航">
        <button type="button" @click="emit('navigate', 'home')">首页</button>
        <span aria-hidden="true">›</span>
        <button type="button" @click="selectSeries('all')">作品</button>
        <template v-if="currentSeries">
          <span aria-hidden="true">›</span>
          <span aria-current="page">{{ currentSeries.name }}</span>
        </template>
      </nav>

      <div class="works-hero__heading">
        <div>
          <p class="section-index">WORKS / SELECTED PAINTINGS</p>
          <h1 id="works-title">作品<span class="serif-italic">目录</span></h1>
        </div>
        <p class="works-hero__intro">
          星球、星云、月相与深空。每一幅画都是一段缓慢的观看，也是一处可供停留的内心坐标。
        </p>
      </div>
    </section>

    <section class="works-catalog page-shell" aria-label="作品筛选与画廊">
      <div class="filter-panel">
        <div class="filter-row">
          <p class="filter-label">系列</p>
          <div class="filter-options" aria-label="按系列筛选">
            <button
              type="button"
              class="filter-chip"
              :class="{ 'filter-chip--active': activeSeries === 'all' }"
              :aria-pressed="activeSeries === 'all'"
              @click="selectSeries('all')"
            >
              全部
            </button>
            <button
              v-for="series in seriesOptions"
              :key="series.id"
              type="button"
              class="filter-chip"
              :class="{ 'filter-chip--active': activeSeries === series.id }"
              :aria-pressed="activeSeries === series.id"
              @click="selectSeries(series.id)"
            >
              {{ series.name }}
            </button>
          </div>
        </div>

        <div class="filter-row">
          <p class="filter-label">媒介</p>
          <div class="filter-options" aria-label="按媒介筛选">
            <button
              v-for="medium in mediaOptions"
              :key="medium"
              type="button"
              class="filter-chip"
              :class="{ 'filter-chip--active': activeMedium === medium }"
              :aria-pressed="activeMedium === medium"
              @click="activeMedium = medium"
            >
              {{ medium === "all" ? "全部" : medium }}
            </button>
          </div>
        </div>

        <div class="filter-summary">
          <p aria-live="polite">
            {{ currentSeries?.name ?? "全部系列" }} · {{ activeMedium === "all" ? "全部媒介" : activeMedium }}
            <span>/ {{ resultSummary }}</span>
          </p>
          <button v-if="hasFilters" class="text-link text-link--small" type="button" @click="resetFilters">
            清除筛选
          </button>
        </div>
      </div>

      <div v-if="filteredWorks.length" class="works-grid">
        <article v-for="(artwork, index) in filteredWorks" :key="artwork.id" class="work-card">
          <button
            class="artwork-frame work-card__image"
            type="button"
            :aria-label="`放大查看《${artwork.title}》`"
            @click="openPreview(artwork.id)"
          >
            <ArtworkImage :artwork="artwork" />
            <span class="work-card__zoom">查看大图</span>
          </button>

          <div class="work-card__body">
            <div class="work-card__topline">
              <span>No. {{ String(index + 1).padStart(2, "0") }}</span>
              <span class="status-pill" :class="statusClass(artwork.status)">
                {{ artwork.status }}
              </span>
            </div>
            <h2>《{{ artwork.title }}》</h2>
            <p class="work-card__details">{{ artwork.year }} · {{ artwork.medium }} · {{ artwork.dimensions }}</p>
            <p class="work-card__note">{{ artwork.note }}</p>
            <p class="copyright">© Léa</p>
            <button class="work-card__consult" type="button" @click="requestCommission(artwork.title)">
              咨询收藏 <span aria-hidden="true">→</span>
            </button>
          </div>
        </article>
      </div>

      <div v-else class="empty-state">
        <p class="section-index">NO MATCHING WORKS</p>
        <h2>暂时没有符合条件的作品</h2>
        <p>可以尝试切换系列或媒介，查看画廊中的其他画作。</p>
        <button class="button button--line" type="button" @click="resetFilters">清除筛选</button>
      </div>

      <aside class="edition-note">
        <p class="section-index">ABOUT EDITIONS</p>
        <div>
          <h2>关于限量版画</h2>
          <p>
            部分原作开放限量版画，每版限量 20 版，附编号与签名，选用收藏级纸张限量发售。
            网站图片仅作线上预览，不代表原作高清文件，屏幕颜色与实体作品可能存在细微差异。
          </p>
        </div>
      </aside>
    </section>

    <Teleport to="body">
      <div
        v-if="modalOpen && currentArtwork"
        class="artwork-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="artwork-modal-title"
        @click.self="closePreview"
      >
        <div class="artwork-modal__panel">
          <button ref="closeButton" class="modal-close" type="button" aria-label="关闭大图预览" @click="closePreview">
            <span></span><span></span>
          </button>

          <div class="artwork-modal__visual">
            <ArtworkImage :artwork="currentArtwork" eager />
          </div>

          <div class="artwork-modal__info">
            <p class="section-index">{{ getSeries(currentArtwork.series)?.english }}</p>
            <h2 id="artwork-modal-title">《{{ currentArtwork.title }}》</h2>
            <p class="artwork-modal__meta">
              {{ currentArtwork.year }}<br />
              {{ currentArtwork.medium }}<br />
              {{ currentArtwork.dimensions }}
            </p>
            <p class="artwork-modal__note">“{{ currentArtwork.note }}”</p>
            <p class="status-pill" :class="statusClass(currentArtwork.status)">
              {{ currentArtwork.status }}
            </p>
            <p v-if="currentArtwork.edition" class="artwork-modal__edition">{{ currentArtwork.edition }}</p>
            <p class="copyright">© Léa</p>
            <button class="button button--dark" type="button" @click="requestCommission(currentArtwork.title)">
              咨询收藏 <span aria-hidden="true">→</span>
            </button>
          </div>

          <div class="artwork-modal__nav" aria-label="切换作品">
            <button type="button" @click="showPrevious">← 上一张</button>
            <span>{{ modalIndex + 1 }} / {{ filteredWorks.length }}</span>
            <button type="button" @click="showNext">下一张 →</button>
          </div>
        </div>
      </div>
    </Teleport>
  </main>
</template>
