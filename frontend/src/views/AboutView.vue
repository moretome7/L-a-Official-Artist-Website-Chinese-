<script setup lang="ts">
import type { RouteName } from "../types";

const emit = defineEmits<{
  navigate: [name: RouteName];
}>();

const media = [
  { name: "油画", english: "Oil", text: "以层层罩染保留光的深度，适合大尺幅与长久观看。" },
  { name: "丙烯", english: "Acrylic", text: "更直接、轻盈的材料，用来记录色彩与情绪的速度。" },
  { name: "数字绘画", english: "Digital", text: "在屏幕中构建光线与颗粒，探索星云的流动边界。" },
  { name: "纸本", english: "Paper", text: "小尺幅的纸面练习，保留手稿般的呼吸与留白。" },
];

const timeline = [
  { year: "2024", title: "星球主题系列", text: "开始系统性地以星球为母题，持续探索记忆、距离与孤独的视觉表达。" },
  { year: "2025", title: "线下群展", text: "系列作品参与线下群展，在更真实的空间中与观看者相遇。" },
  { year: "2026", title: "深空与星云", text: "持续更新深空、星云新作，并将创作延伸至空间与品牌合作。" },
];
</script>

<template>
  <main>
    <section class="about-hero page-shell" aria-labelledby="about-title">
      <nav class="breadcrumb" aria-label="面包屑导航">
        <button type="button" @click="emit('navigate', 'home')">首页</button>
        <span aria-hidden="true">›</span>
        <span aria-current="page">关于</span>
      </nav>

      <div class="about-hero__heading">
        <p class="section-index">ABOUT THE ARTIST</p>
        <h1 id="about-title">关于 <span class="serif-italic">Léa</span></h1>
        <p>画家，独立创作者。以星球、星云与深空为母题，在低饱和的色彩与缓慢的笔触里，描绘时间安静的一面。</p>
      </div>

      <div class="about-portrait-layout">
        <div class="artist-portrait" role="img" aria-label="Léa 工作室与星球绘画的抽象视觉">
          <div class="artist-portrait__orbit artist-portrait__orbit--outer"></div>
          <div class="artist-portrait__orbit artist-portrait__orbit--inner"></div>
          <div class="artist-portrait__planet"></div>
          <span class="artist-portrait__initial">L</span>
          <p>Studio note<br />Quiet light, 2026</p>
        </div>
        <blockquote class="artist-quote">
          <p>“我画星球，也画时间里安静的部分。那些不被言说的孤独、缓慢与辽阔，是我一直想留在画面里的东西。”</p>
          <footer>— Léa</footer>
        </blockquote>
      </div>
    </section>

    <section class="about-statement page-shell" aria-labelledby="artist-statement-title">
      <div class="section-intro">
        <p class="section-index">01 / ARTIST STATEMENT</p>
        <h2 id="artist-statement-title">她的创作，<br />关于宇宙，也关于<span class="serif-italic">内心</span>。</h2>
      </div>
      <div class="prose-block">
        <p>
          Léa 的创作围绕星球、星云与深空意象展开。她试图用绘画捕捉宇宙中安静的部分——那些不被言说的孤独、缓慢与辽阔。
        </p>
        <p>
          对她而言，一颗星球并不只是天体，也可以是记忆、情绪与内心世界的投影。她画星球，也画时间。在巨大的寂静里，寻找属于个体的微小坐标。
        </p>
        <p>
          作品避免强烈的视觉刺激，让颜色、边缘与留白承担更多叙述。观看可以很慢，甚至允许短暂走神；那些在安静中浮现的感受，正是作品希望保留的部分。
        </p>
      </div>
    </section>

    <section class="about-media page-shell" aria-labelledby="media-title">
      <div class="section-heading section-heading--top">
        <div>
          <p class="section-index">02 / MEDIUM</p>
          <h2 id="media-title">常用<span class="serif-italic">创作媒介</span></h2>
        </div>
        <p class="section-note">材料的选择，<br />也是观看方式的选择。</p>
      </div>

      <div class="media-list">
        <article v-for="(item, index) in media" :key="item.name" class="media-item">
          <span class="media-item__index">0{{ index + 1 }}</span>
          <div class="media-item__title">
            <h3>{{ item.name }}</h3>
            <p>{{ item.english }}</p>
          </div>
          <p>{{ item.text }}</p>
        </article>
      </div>
    </section>

    <section class="about-timeline page-shell" aria-labelledby="timeline-title">
      <div class="section-intro">
        <p class="section-index">03 / TIMELINE</p>
        <h2 id="timeline-title">一条<span class="serif-italic">缓慢</span>的创作时间线</h2>
      </div>
      <ol class="timeline-list">
        <li v-for="item in timeline" :key="item.year">
          <span class="timeline-list__year">{{ item.year }}</span>
          <span class="timeline-list__marker" aria-hidden="true"></span>
          <div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </div>
        </li>
      </ol>
    </section>

    <section class="about-journal page-shell" aria-labelledby="journal-title">
      <div class="journal-paper">
        <p class="section-index">04 / STUDIO NOTE</p>
        <h2 id="journal-title">创作随笔</h2>
        <blockquote>今天画这片星云的时候，想的是遥远行星安静的黄昏。</blockquote>
        <p class="journal-paper__date">Studio note · 2026.03</p>
      </div>
      <div class="cv-block">
        <p class="section-index">05 / SELECTED INFORMATION</p>
        <h2>履历</h2>
        <dl>
          <div>
            <dt>展览</dt>
            <dd>个人履历持续更新中</dd>
          </div>
          <div>
            <dt>收藏</dt>
            <dd>作品由私人藏家收藏于中国及海外</dd>
          </div>
          <div>
            <dt>奖项</dt>
            <dd>暂无公开记录</dd>
          </div>
        </dl>
        <button class="text-link" type="button" @click="emit('navigate', 'contact')">
          获取完整作品资料 <span aria-hidden="true">→</span>
        </button>
      </div>
    </section>

    <section class="page-cta page-shell">
      <p class="section-index">VIEW THE WORKS</p>
      <h2>继续走进她的<span class="serif-italic">星球</span></h2>
      <div class="hero-actions">
        <button class="button button--dark" type="button" @click="emit('navigate', 'works')">查看作品</button>
        <button class="button button--line" type="button" @click="emit('navigate', 'commission')">委托创作</button>
      </div>
    </section>
  </main>
</template>