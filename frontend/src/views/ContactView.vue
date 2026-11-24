<script setup lang="ts">
import { computed, ref } from "vue";
import type { RouteName } from "../types";

const emit = defineEmits<{
  navigate: [name: RouteName];
}>();

const contactScopes = [
  { title: "作品收藏", text: "咨询原作、限量版画与现有作品的收藏信息。" },
  { title: "展览邀约", text: "画廊、艺术机构及独立空间的展览与策展合作。" },
  { title: "品牌合作", text: "围绕星球意象展开的视觉、空间与联名合作。" },
  { title: "媒体采访", text: "艺术家访谈、作品报道与内容授权咨询。" },
  { title: "委托约稿", text: "私人收藏、空间绘画、封面插画等委托需求。" },
];

const name = ref("");
const email = ref("");
const message = ref("");
const referenceFileName = ref("");
const formError = ref("");
const submitted = ref(false);

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const mailtoHref = computed(() => {
  const subject = "网站留言｜Léa";
  const body = [
    `姓名：${name.value || "未填写"}`,
    `邮箱：${email.value || "未填写"}`,
    `留言：${message.value || "未填写"}`,
    `参考图：${referenceFileName.value || "邮件中另附"}`,
  ].join("\n");

  return `mailto:769414371@qq.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
});

function handleFileChange(event: Event): void {
  const input = event.target as HTMLInputElement;
  referenceFileName.value = input.files?.[0]?.name ?? "";
}

function submitForm(): void {
  submitted.value = false;
  formError.value = "";

  if (!name.value.trim()) {
    formError.value = "请填写你的姓名。";
    return;
  }

  if (email.value.trim() && !emailPattern.test(email.value.trim())) {
    formError.value = "请填写有效的邮箱地址，或留空。";
    return;
  }

  if (!message.value.trim()) {
    formError.value = "请填写留言内容。";
    return;
  }

  submitted.value = true;
}
</script>

<template>
  <main>
    <section class="contact-hero page-shell" aria-labelledby="contact-title">
      <nav class="breadcrumb" aria-label="面包屑导航">
        <button type="button" @click="emit('navigate', 'home')">首页</button>
        <span aria-hidden="true">›</span>
        <span aria-current="page">联系</span>
      </nav>

      <div class="contact-hero__heading">
        <div>
          <p class="section-index">CONTACT / WRITE TO LÉA</p>
          <h1 id="contact-title">保持<span class="serif-italic">联系</span></h1>
        </div>
        <p class="contact-hero__intro">
          无论是收藏一幅作品、讨论一次合作，还是想聊聊某个尚未成形的想法，都欢迎写信。
          邮件通常会在 3–5 个工作日内得到回复。
        </p>
      </div>

      <div class="contact-grid">
        <div class="contact-primary">
          <p class="section-index">01 / EMAIL</p>
          <a class="contact-email" href="mailto:769414371@qq.com">769414371@qq.com <span aria-hidden="true">↗</span></a>
          <p>电子邮件是联系 Léa 最直接的方式。附件可包含作品参考、空间照片或项目资料。</p>
          <div class="contact-socials" aria-label="社交媒体">
            <a href="https://www.xiaohongshu.com/" target="_blank" rel="noreferrer">小红书 <span aria-hidden="true">↗</span></a>
            <a href="https://www.instagram.com/" target="_blank" rel="noreferrer">Instagram <span aria-hidden="true">↗</span></a>
          </div>
        </div>

        <div class="contact-scope">
          <p class="section-index">02 / ENQUIRIES</p>
          <h2>可咨询<span class="serif-italic">范围</span></h2>
          <ol class="contact-scope-list">
            <li v-for="(item, index) in contactScopes" :key="item.title">
              <span>0{{ index + 1 }}</span>
              <div>
                <h3>{{ item.title }}</h3>
                <p>{{ item.text }}</p>
              </div>
            </li>
          </ol>
        </div>
      </div>
    </section>

    <section id="contact-form" class="form-section page-shell" aria-labelledby="contact-form-title">
      <div class="form-intro">
        <p class="section-index">03 / MESSAGE</p>
        <h2 id="contact-form-title">留下你的<span class="serif-italic">留言</span></h2>
        <p>请说明咨询主题与大致需求。若计划附上参考图，可在邮件中一并发送。</p>
        <p class="form-privacy">您提交的信息仅用于本次沟通，不会对外泄露。</p>
      </div>

      <form class="enquiry-form" novalidate @submit.prevent="submitForm">
        <div class="form-grid form-grid--two">
          <label class="field">
            <span>姓名 <em>*</em></span>
            <input v-model="name" type="text" name="name" autocomplete="name" placeholder="如何称呼你" />
          </label>
          <label class="field">
            <span>邮箱 <small>（选填）</small></span>
            <input v-model="email" type="email" name="email" autocomplete="email" placeholder="name@example.com" />
          </label>
        </div>

        <label class="field">
          <span>留言内容 <em>*</em></span>
          <textarea
            v-model="message"
            name="message"
            rows="6"
            placeholder="咨询主题、项目背景、期望回复方式，或任何想说的话"
          ></textarea>
        </label>

        <label class="field field--file">
          <span>上传参考图</span>
          <span class="file-input-wrap">
            <span class="file-input-label">选择文件</span>
            <input type="file" name="reference" accept="image/*" @change="handleFileChange" />
            <span class="file-input-name">{{ referenceFileName || "未选择文件" }}</span>
          </span>
          <small>参考图仅用于沟通方向；当前为纯前端页面，不会实际上传文件，请在邮件中另附。</small>
        </label>

        <p v-if="formError" class="form-message form-message--error" role="alert">{{ formError }}</p>
        <div v-if="submitted" class="form-success" role="status">
          <p>留言已在当前页面完成预览。当前为纯前端演示，信息尚未真正发送。</p>
          <a class="button button--dark" :href="mailtoHref">通过邮件发送留言 <span aria-hidden="true">↗</span></a>
        </div>

        <div class="form-actions">
          <button class="button button--dark" type="submit">准备邮件内容 <span aria-hidden="true">→</span></button>
          <p>或直接写信至 <a href="mailto:769414371@qq.com">769414371@qq.com</a></p>
        </div>
      </form>
    </section>

    <section class="page-cta page-shell contact-cta">
      <p class="section-index">A QUIET INVITATION</p>
      <h2>期待与你，在<span class="serif-italic">同一片星空</span>下相遇。</h2>
      <div class="hero-actions">
        <button class="button button--line" type="button" @click="emit('navigate', 'works')">浏览作品</button>
        <button class="button button--dark" type="button" @click="emit('navigate', 'commission')">了解委托</button>
      </div>
    </section>
  </main>
</template>