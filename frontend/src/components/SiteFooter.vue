<script setup lang="ts">
import type { RouteName } from "../types";

const emit = defineEmits<{
  navigate: [name: RouteName];
}>();
</script>

<template>
  <footer class="site-footer">
    <div class="footer-main">
      <button class="footer-wordmark" type="button" aria-label="返回首页" @click="emit('navigate', 'home')">
        Léa<span>.</span>
      </button>
      <p class="footer-slogan">她画星球，<br />也画时间里安静的部分。</p>
      <div class="footer-links" aria-label="页脚导航">
        <button type="button" @click="emit('navigate', 'works')">作品</button>
        <button type="button" @click="emit('navigate', 'about')">关于</button>
        <button type="button" @click="emit('navigate', 'commission')">委托</button>
        <button type="button" @click="emit('navigate', 'contact')">联系</button>
      </div>
      <div class="footer-social">
        <a href="mailto:769414371@qq.com" aria-label="发送邮件至 Léa">Email</a>
        <a href="https://www.instagram.com/" target="_blank" rel="noreferrer" aria-label="Instagram（新窗口）">Instagram ↗</a>
        <a href="https://www.xiaohongshu.com/" target="_blank" rel="noreferrer" aria-label="小红书（新窗口）">小红书 ↗</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Léa © 2026 All Rights Reserved</p>
      <p>Artist &amp; Painter · China</p>
      <a href="mailto:769414371@qq.com">769414371@qq.com</a>
    </div>
  </footer>
</template>