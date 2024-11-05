<script setup>
definePageMeta({
  layout: 'empty'
});

</script>

<!-- Tela inicial -->
<template>
  <div class="flex justify-between w-full h-screen">

    <div class="flex flex-col justify-center w-1/2 bg-customBlue h-full items-center">
      <LogoLand width="w-80" />
      <h1 class="text-white text-4xl font-bold">Cross The Line</h1>
    </div>

    <div class="flex flex-col justify-center w-1/2 items-center space-y-16">
      <LandingPageButton iconName="mdi:chart-timeline-variant-shimmer" label="Previsão Diária" bgColor="bg-customGreen"
        redirect="/prediction" />
      <LandingPageButton iconName="mdi:clipboard-text-outline" label="Histórico" redirect="/history" />
      <LandingPageButton iconName="mdi:view-dashboard-outline" label="Dashboard" redirect="/dashboard" />
      <LandingPageButton iconName="mdi:progress-download" label="Treinamento Mensal" redirect="/monthly" />
      <LandingPageButton iconName="mdi:folder-wrench" label="Escolha de Modelos" redirect="/chooseModel" />

    </div>
  </div>
</template>
