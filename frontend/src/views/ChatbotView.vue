<script setup>
import LeftSection from '@/components/Chatbot/LeftSection.vue'
import RightSection from '@/components/Chatbot/rightsection/RightSectionMain.vue'
</script>

<template>
  <div class="container-fluid d-flex flex-row m-0 p-0">
    <div class="p-0">
      <left-section />
    </div>
    <div class="right-section-wrapper d-flex justify-content-center align-items-center p-0 m-0">
      <RightSection />
    </div>
  </div>
</template>

<style scoped>
.right-section-wrapper {
  flex-grow: 1; /* 나머지 공간을 차지하도록 설정 */
  display: flex;
  justify-content: center; /* 수평 중앙 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
}
</style>
