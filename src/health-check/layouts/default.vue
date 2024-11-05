<script>
import normalLogo from '@/assets/static/logo.png';
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <!-- Header with fixed positioning -->
    <header class="fixed top-0 left-0 right-0 border-b-2 border-customBlue flex items-center p-4 bg-white z-50">
      <!-- Div on the left with the Logo and project name -->
      <div class="hover:scale-[101%] transition cursor-pointer flex items-center mr-12 ">
        <Logo width="w-12" :logo="normalLogo" class="mt-1"/>
        <p class="font-bold text-base">Cross The Line</p>
      </div>
    </header>

    <!-- Page content area -->
    <div class="flex-grow p-4 mt-16 "> <!-- Added margin-top to offset the fixed header -->
      <div class="min-h-[80vh]"> 
        <slot /> <!-- Page content -->
      </div>
    </div>

    <!-- Page footer -->
    <footer class="relative w-full bg-gray-800 text-white py-4 flex items-center justify-center">
      <p class="absolute left-1/2 transform -translate-x-1/2">&copy; 2024 Cross The Line. Todos direitos reservados.</p>
      <p class="ml-auto mr-2">Github</p>
      <a href="https://github.com/Inteli-College/2024-2A-T08-EC07-G01" target="_blank" class="ml-4">
        <Icon name="mdi:github" class="text-white text-2xl ml-auto mr-12 mt-1" />
      </a>
    </footer>
  </div>
</template>
