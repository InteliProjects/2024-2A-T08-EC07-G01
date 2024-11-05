<template>
  <div class="flex flex-col  justify-center w-1/2 items-center">
    <h1 class="text-4xl font-bold text-customBlue mb-4">Health Check</h1>
    <p class="text-lg text-gray-700 mb-8">Verifique a saúde do seu sistema</p>
    <h2 class="m-0 text-2xl font-semibold text-gray-900 mb-8">Serviços Disponíveis:</h2>
    <ul class="space-y-6 w-1/2">
      <li class="flex justify-between p-4 bg-white shadow-md rounded-lg">
        <span class="font-medium mr-8 text-gray-700">FrontEnd</span>
        <span
          :class="{ 'text-red-500': frontendStatus !== 'Status: 200', 'text-green-500': frontendStatus === 'Status: 200' }"
          class="font-semibold">{{ frontendStatus === 'Status: 200' ? 'Status: OK' : frontendStatus }}</span>
      </li>
      <li class="flex justify-between p-4 bg-white shadow-md rounded-lg">
        <span class="font-medium mr-8 text-gray-700">BackEnd</span>
        <span
          :class="{ 'text-red-500': backendStatus !== 'Status: 200', 'text-green-500': backendStatus === 'Status: 200' }"
          class="font-semibold">{{ backendStatus === 'Status: 200' ? 'Status: OK' : backendStatus }}</span>
      </li>
      <li class="flex justify-between p-4 bg-white shadow-md rounded-lg">
        <span class="font-medium mr-8 text-gray-700">MongoDB</span>
        <span
          :class="{ 'text-red-500': databaseStatus !== 'Status: 200', 'text-green-500': databaseStatus === 'Status: 200' }"
          class="font-semibold">{{ databaseStatus === 'Status: 200' ? 'Status: OK' : databaseStatus }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      backendStatus: '',
      databaseStatus: '',
      frontendStatus: '',
      intervalId: null, // Salvando o ID do intervalo para limpar posteriormente
    };
  },
  mounted() {
    // Verifica os serviços imediatamente e depois a cada 1 segundo
    this.fetchAllServices();
    this.intervalId = setInterval(() => this.fetchAllServices(), 30000);
  },
  beforeUnmount() {
    // Limpa o intervalo quando o componente é destruído
    clearInterval(this.intervalId);
  },
  methods: {
    async fetchBackendStatus() {
      try {
        const response = await fetch('http://localhost:8000/');
        this.backendStatus = `Status: ${response.status}`;
      } catch (error) {
        console.error('Error fetching backend data:', error);
        this.backendStatus = 'Status: Error';
      }
    },
    async fetchDatabaseStatus() {
      try {
        const response = await fetch('http://localhost:8000/healthcheck/mongodb', {
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        const statusCode = data.status_code;
        console.log(`Database status: ${statusCode}`);
        
        this.databaseStatus = `Status: ${statusCode}`;
      } catch (error) {
        console.error('Error fetching database data:', error);
        this.databaseStatus = 'Status: Error';
      }
    },
    async fetchFrontendStatus() {
      try {
        const response = await fetch('http://localhost:3000/', {
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          credentials: 'include'
        });
        console.log(response)
        this.frontendStatus = `Status: ${response.status}`;
      } catch (error) {
        console.error('Error fetching frontend data:', error);
        this.frontendStatus = 'Status: Error';
      }
    },
    async fetchAllServices() {
      await Promise.all([
        this.fetchBackendStatus(),
        this.fetchDatabaseStatus(),
        this.fetchFrontendStatus(),
      ]);
    },
  },
};
</script>
