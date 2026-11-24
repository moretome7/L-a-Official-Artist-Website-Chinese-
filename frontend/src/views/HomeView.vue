<script setup lang="ts">
import ArtworkImage from "../components/ArtworkImage.vue";
import { featuredWorks, seriesOptions, works } from "../data/works";
import type { RouteName, SeriesId } from "../types";

const emit = defineEmits<{
  navigate: [name: RouteName];
  openWork: [workId: string];
  openSeries: [seriesId: SeriesId];
}>();

const representative = featuredWorks[0];
const latestWorks = [works[9], works[12], works[14]];
</script>

<template>
  <main>
    <section class="home-hero page-shell" aria-labelledby="home-title">
      <div class="home-hero__introduction">
        <p class="eyebrow">Planet · Nebula · Deep Space</p>
        <p class="home-hero__name" aria-hidden="true">Léa</p>
        <h1 id="home-title">她画星球，<br />也画时间里<span class="serif-italic">安静的部分</span>。</h1>
        <p class="home-hero__lede">
          以绘画记录宇宙的安静与辽阔。在巨大的寂静里，寻找属于个体的微小坐标。
        </p>
        <div class="hero-actions">
          <button class="button button--dark" type="button" @click="emit('navigate', 'works')">
            查看作品 <span aria-hidden="true">↗</span>
          </button>
          <button class="button button--line" type="button" @click="emit('navigate', 'commission')">
            了解委托
          </button>
        </div>
        <div class="home-hero__meta" aria-label="艺术家信息">
          <span>Artist &amp; Painter</span>
          <span>Based in China</span>
          <span>Working since 2023</span>
        </div>
      </div>

      <button
        class="home-hero__artwork artwork-frame artwork-frame--feature"
        type="button"
        :aria-label="`查看代表作《${representative.title}》`"
        @click="emit('openWork', representative.id)"
      >
        <ArtworkImage :artwork="representative" eager />
        <span class="home-hero__artwork-caption">
          <span>
            <strong>《{{ representative.title }}》</strong>
            <small>{{ representative.year }} · {{ representative.medium }}</small>
          </span>
          <span class="text-arrow" aria-hidden="true">↗</span>
        </span>
      </button>

      <p class="home-hero__guide">Selected work<br />No. 07</p>
    </section>

    <section class="home-statement page-shell" aria-labelledby="statement-title">
      <div class="section-intro">
        <p class="section-index">01 / ARTIST STATEMENT</p>
        <h2 id="statement-title">在遥远与微小之间，<br />保留一块<span class="serif-italic">安静的地方</span>。</h2>
      </div>
      <div class="home-statement__copy">
        <p>
          Léa 的创作围绕星球、星云与深空意象展开。她试图捕捉宇宙中不被言说的孤独、缓慢与辽阔。
        </p>
        <p>
          一颗星球并不只是天体，也可以是记忆、情绪与内心世界的投影。作品在不喧哗的色彩里，留下可以被长久凝望的空间。
        </p>
        <button class="text-link" type="button" @click="emit('navigate', 'about')">
          阅读艺术家自述 <span aria-hidden="true">→</span>
        </button>
      </div>
    </section>

    <section class="home-latest page-shell" aria-labelledby="latest-title">
      <div class="section-heading">
        <div>
          <p class="section-index">02 / RECENT WORKS</p>
          <h2 id="latest-title">新作，<span class="serif-italic">静候凝视</span></h2>
        </div>
        <p class="section-note">新作不定期更新<br />作品图片仅供线上预览</p>
      </div>

      <div class="latest-grid">
        <button
          v-for="(artwork, index) in latestWorks"
          :key="artwork.id"
          class="latest-card"
          type="button"
          :aria-label="`查看《${artwork.title}》`"
          @click="emit('openWork', artwork.id)"
        >
          <span class="artwork-frame">
            <ArtworkImage :artwork="artwork" compact />
          </span>
          <span class="latest-card__info">
            <span class="latest-card__number">0{{ index + 1 }}</span>
            <span>
              <strong>《{{ artwork.title }}》</strong>
              <small>{{ artwork.year }} · {{ artwork.medium }}</small>
            </span>
            <span class="text-arrow" aria-hidden="true">↗</span>
          </span>
        </button>
      </div>
    </section>

    <section class="home-series page-shell" aria-labelledby="series-title">
      <div class="section-heading section-heading--top">
        <div>
          <p class="section-index">03 / SERIES</p>
          <h2 id="series-title">四个关于宇宙的<span class="serif-italic">观看方式</span></h2>
        </div>
        <button class="text-link" type="button" @click="emit('navigate', 'works')">
          浏览全部作品 <span aria-hidden="true">→</span>
        </button>
      </div>

      <div class="series-index">
        <button
          v-for="(series, index) in seriesOptions"
          :key="series.id"
          class="series-index__item"
          type="button"
          @click="emit('openSeries', series.id)"
        >
          <span class="series-index__number">0{{ index + 1 }}</span>
          <span class="series-index__name">
            <strong>{{ series.name }}</strong>
            <small>{{ series.english }}</small>
          </span>
          <span class="series-index__description">{{ series.description }}</span>
          <span class="text-arrow" aria-hidden="true">↗</span>
        </button>
      </div>
    </section>

    <section class="home-commission page-shell">
      <div class="home-commission__orb" aria-hidden="true"></div>
      <div class="home-commission__copy">
        <p class="section-index">04 / COMMISSION</p>
        <h2>把一颗只属于你的星球，<br />留在<span class="serif-italic">日常里</span>。</h2>
        <p>私人收藏、空间装饰、封面插画与品牌合作，均可提交需求。通常在 3–5 个工作日内回复。</p>
        <button class="button button--dark" type="button" @click="emit('navigate', 'commission')">
          了解委托方式 <span aria-hidden="true">↗</span>
        </button>
      </div>
    </section>
  </main>
</template>