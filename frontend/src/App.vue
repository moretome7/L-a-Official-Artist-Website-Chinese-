<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref } from "vue";
import SiteFooter from "./components/SiteFooter.vue";
import SiteHeader from "./components/SiteHeader.vue";
import { works } from "./data/works";
import type { RouteName, SeriesId } from "./types";
import AboutView from "./views/AboutView.vue";
import CommissionView from "./views/CommissionView.vue";
import ContactView from "./views/ContactView.vue";
import HomeView from "./views/HomeView.vue";
import WorksView from "./views/WorksView.vue";

const routes: RouteName[] = ["home", "works", "about", "commission", "contact"];

const pageTitles: Record<RouteName, string> = {
  home: "Léa｜以绘画记录宇宙的安静",
  works: "作品｜Léa",
  about: "关于｜Léa",
  commission: "委托创作｜Léa",
  contact: "联系｜Léa",
};

function readRoute(): RouteName {
  const name = window.location.hash.replace(/^#\/?/, "").split("?")[0];
  return routes.includes(name as RouteName) ? (name as RouteName) : "home";
}

const route = ref<RouteName>(readRoute());
const menuOpen = ref(false);
const selectedSeries = ref<SeriesId | "all">("all");
const selectedWorkId = ref("");
const selectedWorkTitle = ref("");
const selectedCommissionType = ref("");
const worksRevision = ref(0);

function applyRoute(name: RouteName): void {
  route.value = name;
  document.title = pageTitles[name];
  nextTick(() => window.scrollTo({ top: 0, behavior: "auto" }));
}

function goTo(name: RouteName): void {
  menuOpen.value = false;
  const nextHash = `#/${name}`;

  if (window.location.hash === nextHash) {
    applyRoute(name);
    return;
  }

  window.location.hash = nextHash;
}

function resetWorkContext(): void {
  selectedSeries.value = "all";
  selectedWorkId.value = "";
  selectedWorkTitle.value = "";
  worksRevision.value += 1;
}

function navigate(name: RouteName): void {
  if (name === "works") resetWorkContext();
  if (name === "commission") {
    selectedWorkTitle.value = "";
    selectedCommissionType.value = "";
  }

  goTo(name);
}

function openWork(workId: string): void {
  const artwork = works.find((item) => item.id === workId);
  if (!artwork) return;

  selectedSeries.value = artwork.series;
  selectedWorkId.value = artwork.id;
  selectedWorkTitle.value = artwork.title;
  worksRevision.value += 1;
  goTo("works");
}

function openSeries(seriesId: SeriesId): void {
  selectedSeries.value = seriesId;
  selectedWorkId.value = "";
  selectedWorkTitle.value = "";
  worksRevision.value += 1;
  goTo("works");
}

function consult(workTitle: string): void {
  selectedWorkTitle.value = workTitle;
  selectedCommissionType.value = "私人收藏";
  goTo("commission");
}

function onHashChange(): void {
  menuOpen.value = false;
  applyRoute(readRoute());
}

onMounted(() => {
  applyRoute(route.value);
  window.addEventListener("hashchange", onHashChange);
});

onBeforeUnmount(() => {
  window.removeEventListener("hashchange", onHashChange);
});
</script>

<template>
  <div class="site-shell">
    <SiteHeader
      :route="route"
      :menu-open="menuOpen"
      @navigate="navigate"
      @toggle-menu="menuOpen = !menuOpen"
    />

    <div class="route-view">
      <HomeView
        v-if="route === 'home'"
        @navigate="navigate"
        @open-work="openWork"
        @open-series="openSeries"
      />
      <WorksView
        v-else-if="route === 'works'"
        :key="worksRevision"
        :initial-series="selectedSeries"
        :initial-work-id="selectedWorkId"
        @navigate="navigate"
        @consult="consult"
      />
      <AboutView v-else-if="route === 'about'" @navigate="navigate" />
      <CommissionView
        v-else-if="route === 'commission'"
        :initial-work-title="selectedWorkTitle"
        :initial-commission-type="selectedCommissionType"
        @navigate="navigate"
      />
      <ContactView v-else @navigate="navigate" />
    </div>

    <SiteFooter @navigate="navigate" />
  </div>
</template>