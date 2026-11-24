<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import type { RouteName } from "../types";

const props = defineProps<{
  route: RouteName;
  menuOpen: boolean;
}>();

const emit = defineEmits<{
  navigate: [name: RouteName];
  toggleMenu: [];
}>();

const scrolled = ref(false);
const links: Array<{ name: RouteName; label: string }> = [
  { name: "home", label: "首页" },
  { name: "works", label: "作品" },
  { name: "about", label: "关于" },
  { name: "commission", label: "委托" },
  { name: "contact", label: "联系" },
];

const isScrolled = computed(() => scrolled.value || props.menuOpen);

function onScroll(): void {
  scrolled.value = window.scrollY > 16;
}

onMounted(() => {
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", onScroll);
});
</script>

<template>
  <header class="site-header" :class="{ 'site-header--scrolled': isScrolled, 'site-header--menu-open': menuOpen }">
    <div class="header-inner">
      <button class="wordmark" type="button" aria-label="Léa 首页" @click="emit('navigate', 'home')">
        Léa<span class="wordmark-dot">.</span>
      </button>

      <nav class="desktop-nav" aria-label="主导航">
        <button
          v-for="link in links"
          :key="link.name"
          type="button"
          class="nav-link"
          :class="{ 'nav-link--active': route === link.name }"
          :aria-current="route === link.name ? 'page' : undefined"
          @click="emit('navigate', link.name)"
        >
          {{ link.label }}
        </button>
      </nav>

      <button
        class="menu-toggle"
        type="button"
        :aria-expanded="menuOpen"
        aria-controls="mobile-navigation"
        :aria-label="menuOpen ? '关闭导航菜单' : '打开导航菜单'"
        @click="emit('toggleMenu')"
      >
        <span></span>
        <span></span>
      </button>
    </div>

    <nav
      v-if="menuOpen"
      id="mobile-navigation"
      class="mobile-nav"
      aria-label="移动端主导航"
    >
      <button
        v-for="(link, index) in links"
        :key="link.name"
        type="button"
        class="mobile-nav-link"
        :class="{ 'mobile-nav-link--active': route === link.name }"
        @click="emit('navigate', link.name)"
      >
        <span>0{{ index + 1 }}</span>
        {{ link.label }}
      </button>
      <p class="mobile-nav-foot">以绘画记录宇宙的安静与辽阔</p>
    </nav>
  </header>
</template>