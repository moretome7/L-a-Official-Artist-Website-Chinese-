<script setup lang="ts">
import { computed, ref, watch } from "vue";
import ArtworkImage from "../components/ArtworkImage.vue";
import { works } from "../data/works";
import type { RouteName } from "../types";

const emit = defineEmits<{
  navigate: [name: RouteName];
}>();

const props = withDefaults(
  defineProps<{
    initialWorkTitle?: string;
    initialCommissionType?: string;
  }>(),
  {
    initialWorkTitle: "",
    initialCommissionType: "",
  },
);

const commissionTypes = [
  {
    title: "私人收藏",
    english: "Private Collection",
    description: "为个人空间或私人收藏创作一幅星球主题原作，非商用。",
  },
  {
    title: "空间装饰",
    english: "Spatial Artwork",
    description: "为住宅、酒店、会所等空间定制与场域气质相合的画作。",
  },
  {
    title: "书籍封面插画",
    english: "Book Cover",
    description: "为出版物、诗集或独立刊物创作封面视觉与系列插画。",
  },
  {
    title: "品牌视觉合作",
    english: "Brand Collaboration",
    description: "围绕星球意象展开的视觉提案、主视觉与联名合作。",
  },
  {
    title: "展览邀约",
    english: "Exhibition",
    description: "接受画廊、机构和独立空间的主题展览与策展合作邀约。",
  },
];

const commissionCases = [works[0], works[4], works[13]];

const processSteps = [
  { number: "01", title: "提交需求", text: "通过表单或邮件说明你的空间、用途与初步想法。" },
  { number: "02", title: "确认方向", text: "共同确认主题、尺寸、媒介与商用属性。" },
  { number: "03", title: "方案与报价", text: "提供创作方向与报价，通常在 3–5 个工作日内回复。" },
  { number: "04", title: "支付定金", text: "确认合作后支付定金，作品进入创作排期。" },
  { number: "05", title: "创作推进", text: "分享阶段进展，包含 2 次免费微调。" },
  { number: "06", title: "成品交付", text: "完成作品、包装与交付，原作附收藏证书。" },
];

const faqs = [
  {
    question: "原作是否包邮？",
    answer: "国内包邮，海外运费单独核算；具体物流方式会在确认订单时一并说明。",
  },
  {
    question: "版画是限量多少版？",
    answer: "版画每版限量 20 版，附带编号与签名，选用收藏级纸张限量发售。",
  },
  {
    question: "委托交付包含原图文件吗？",
    answer: "私人委托交付成品实体；商用委托会根据授权范围约定文件交付内容。",
  },
  {
    question: "收藏作品会附带证书吗？",
    answer: "所有原作交付均附带手写签名的收藏证书。",
  },
];

const notAccepted = [
  "不接 Q 版、人设、二次元插画",
  "不接低于约定工期的超短加急单",
  "不接侵权或商用范围模糊的需求",
  "不接修改次数无上限的需求",
];

const name = ref("");
const email = ref("");
const commissionType = ref(props.initialCommissionType || "私人收藏");
const commercial = ref("私人非商用");
const dimensions = ref("");
const palette = ref("");
const notes = ref(props.initialWorkTitle ? `咨询作品：《${props.initialWorkTitle}》` : "");
const referenceFileName = ref("");
const formError = ref("");
const submitted = ref(false);

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const mailtoHref = computed(() => {
  const subject = props.initialWorkTitle ? `委托咨询｜${props.initialWorkTitle}` : "委托咨询";
  const body = [
    `称呼：${name.value || "未填写"}`,
    `邮箱：${email.value || "未填写"}`,
    `委托类型：${commissionType.value}`,
    `使用属性：${commercial.value}`,
    `尺寸需求：${dimensions.value || "未填写"}`,
    `偏好色调：${palette.value || "未填写"}`,
    `备注：${notes.value || "未填写"}`,
    `参考图：${referenceFileName.value || "邮件中另附"}`,
  ].join("\n");

  return `mailto:769414371@qq.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
});

watch(
  () => props.initialWorkTitle,
  (title) => {
    if (title) notes.value = `咨询作品：《${title}》`;
  },
);

watch(
  () => props.initialCommissionType,
  (type) => {
    if (type) commissionType.value = type;
  },
);

function handleFileChange(event: Event): void {
  const input = event.target as HTMLInputElement;
  referenceFileName.value = input.files?.[0]?.name ?? "";
}

function submitForm(): void {
  submitted.value = false;
  formError.value = "";

  if (!name.value.trim()) {
    formError.value = "请填写你的称呼。";
    return;
  }
  if (!emailPattern.test(email.value.trim())) {
    formError.value = "请填写有效的邮箱地址。";
    return;
  }
  if (!commissionType.value) {
    formError.value = "请选择委托类型。";
    return;
  }

  submitted.value = true;
}

function chooseType(title: string): void {
  commissionType.value = title;
  document.querySelector("#commission-form")?.scrollIntoView({ behavior: "auto", block: "start" });
}
</script>

<template>
  <main>
    <section class="commission-hero page-shell" aria-labelledby="commission-title">
      <nav class="breadcrumb" aria-label="面包屑导航">
        <button type="button" @click="emit('navigate', 'home')">首页</button>
        <span aria-hidden="true">›</span>
        <span aria-current="page">委托</span>
      </nav>

      <div class="commission-hero__heading">
        <div>
          <p class="section-index">COMMISSIONS / BY REQUEST</p>
          <h1 id="commission-title">委托<span class="serif-italic">创作</span></h1>
        </div>
        <p class="commission-hero__intro">
          把一段记忆、一处空间，或一颗尚未命名的星球，交给缓慢而具体的绘画过程。
          私人收藏与商业合作分开沟通，通常在 3–5 个工作日内回复。
        </p>
      </div>
    </section>

    <section class="commission-types page-shell" aria-labelledby="types-title">
      <div class="section-heading section-heading--top">
        <div>
          <p class="section-index">01 / ACCEPTED PROJECTS</p>
          <h2 id="types-title">可以一起完成的<span class="serif-italic">事情</span></h2>
        </div>
        <p class="section-note">私人 · 空间 · 出版 · 商业 · 展览</p>
      </div>

      <div class="commission-type-grid">
        <article v-for="(item, index) in commissionTypes" :key="item.title" class="commission-type-card">
          <div class="commission-type-card__top">
            <span>0{{ index + 1 }}</span>
            <span>{{ item.english }}</span>
          </div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <button class="text-link text-link--small" type="button" @click="chooseType(item.title)">
            选择此类型 <span aria-hidden="true">→</span>
          </button>
        </article>
      </div>
    </section>

    <section class="commission-cases page-shell" aria-labelledby="cases-title">
      <div class="section-heading section-heading--top">
        <div>
          <p class="section-index">02 / SELECTED REFERENCES</p>
          <h2 id="cases-title">过往委托<span class="serif-italic">参考</span></h2>
        </div>
        <p class="section-note">更多案例可在邮件中索取<br />图片仅作视觉方向参考</p>
      </div>

      <div class="commission-case-grid">
        <article v-for="(artwork, index) in commissionCases" :key="artwork.id" class="commission-case-card">
          <div class="artwork-frame">
            <ArtworkImage :artwork="artwork" compact />
          </div>
          <div class="commission-case-card__caption">
            <span>0{{ index + 1 }} / {{ artwork.year }}</span>
            <h3>《{{ artwork.title }}》</h3>
            <p>{{ artwork.medium }} · {{ artwork.dimensions }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="commission-process page-shell" aria-labelledby="process-title">
      <div class="section-intro">
        <p class="section-index">03 / PROCESS</p>
        <h2 id="process-title">从一句想法，<br />到一件可以<span class="serif-italic">长久留下</span>的作品。</h2>
      </div>
      <ol class="process-list">
        <li v-for="step in processSteps" :key="step.number">
          <span class="process-list__number">{{ step.number }}</span>
          <div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </div>
        </li>
      </ol>
    </section>

    <section class="commission-terms page-shell" aria-label="委托说明">
      <div class="quote-note">
        <p class="section-index">04 / QUOTATION</p>
        <h2>报价与<span class="serif-italic">边界</span></h2>
        <p>
          私人收藏与商业合作分开定价，价格根据尺寸、媒介、创作周期与商用用途决定。
          额外修改单独计费，报价与执行范围会在开始前确认。
        </p>
      </div>
      <div class="not-accepted">
        <p class="section-index">05 / NOT ACCEPTED</p>
        <h2>暂不承接</h2>
        <ul>
          <li v-for="item in notAccepted" :key="item"><span aria-hidden="true">×</span>{{ item }}</li>
        </ul>
      </div>
    </section>

    <section class="commission-faq page-shell" aria-labelledby="commission-faq-title">
      <div class="section-intro">
        <p class="section-index">06 / FAQ</p>
        <h2 id="commission-faq-title">常见<span class="serif-italic">问题</span></h2>
      </div>
      <div class="faq-list">
        <details v-for="faq in faqs" :key="faq.question" class="faq-item">
          <summary>{{ faq.question }}<span aria-hidden="true">+</span></summary>
          <p>{{ faq.answer }}</p>
        </details>
      </div>
    </section>

    <section id="commission-form" class="form-section page-shell" aria-labelledby="form-title">
      <div class="form-intro">
        <p class="section-index">07 / ENQUIRY</p>
        <h2 id="form-title">留下你的<span class="serif-italic">需求</span></h2>
        <p>请尽量说明使用场景、尺寸与期望时间。表单提交后，可在邮件中补充参考图与更完整的资料。</p>
        <p class="form-privacy">您提交的信息仅用于本次沟通，不会对外泄露。</p>
      </div>

      <form class="enquiry-form" novalidate @submit.prevent="submitForm">
        <div class="form-grid form-grid--two">
          <label class="field">
            <span>称呼 <em>*</em></span>
            <input v-model="name" type="text" name="name" autocomplete="name" placeholder="如何称呼你" />
          </label>
          <label class="field">
            <span>邮箱 <em>*</em></span>
            <input v-model="email" type="email" name="email" autocomplete="email" placeholder="name@example.com" />
          </label>
        </div>

        <div class="form-grid form-grid--two">
          <label class="field">
            <span>委托类型 <em>*</em></span>
            <select v-model="commissionType" name="commissionType">
              <option v-for="item in commissionTypes" :key="item.title" :value="item.title">{{ item.title }}</option>
            </select>
          </label>
          <label class="field">
            <span>使用属性 <em>*</em></span>
            <select v-model="commercial" name="commercial">
              <option>私人非商用</option>
              <option>商用授权</option>
              <option>展览 / 机构</option>
            </select>
          </label>
        </div>

        <div class="form-grid form-grid--two">
          <label class="field">
            <span>尺寸需求</span>
            <input v-model="dimensions" type="text" name="dimensions" placeholder="例如 60 × 75 cm，或希望的空间尺寸" />
          </label>
          <label class="field">
            <span>偏好色调</span>
            <input v-model="palette" type="text" name="palette" placeholder="例如 雾蓝、灰紫、低饱和暖灰" />
          </label>
        </div>

        <label class="field">
          <span>备注</span>
          <textarea v-model="notes" name="notes" rows="4" placeholder="项目背景、使用空间、期望交付时间，或任何想说的想法"></textarea>
        </label>

        <label class="field field--file">
          <span>上传参考图</span>
          <span class="file-input-wrap">
            <span class="file-input-label">选择文件</span>
            <input type="file" name="reference" accept="image/*" @change="handleFileChange" />
            <span class="file-input-name">{{ referenceFileName || "未选择文件" }}</span>
          </span>
          <small>参考图仅用于沟通方向；本页面不会直接上传文件，请在邮件中另附。</small>
        </label>

        <p v-if="formError" class="form-message form-message--error" role="alert">{{ formError }}</p>
        <div v-if="submitted" class="form-success" role="status">
          <p>需求信息已在当前页面完成预览。当前为纯前端演示版本，信息尚未真正发送。</p>
          <a class="button button--dark" :href="mailtoHref">通过邮件发送需求 <span aria-hidden="true">↗</span></a>
        </div>

        <div class="form-actions">
          <button class="button button--dark" type="submit">准备邮件内容 <span aria-hidden="true">→</span></button>
          <p>或直接写信至 <a href="mailto:769414371@qq.com">769414371@qq.com</a></p>
        </div>
      </form>
    </section>
  </main>
</template>
