// knrsData.ts
export interface KNRData {
  knr: string;
  hasFailure: boolean;
  failureType: string | null;
}

import { ref, onMounted, computed } from "vue";

export const failTypes = ref([
  {
    failType: 1,
    title: "Tipo 1",
    description: "Parte Traseira",
    status: "default",
  },
  {
    failType: 2,
    title: "Tipo 2",
    description: "Parte Central",
    status: "default",
  },
  {
    failType: 3,
    title: "Tipo 4",
    description: "Portas",
    status: "default",
  },
  {
    failType: 4,
    title: "Tipo 5",
    description: "Parte Dianteira",
    status: "default",
  },
  {
    failType: 5,
    title: "Tipo 133",
    description: "Geral",
    status: "default",
  },
  {
    failType: 6,
    title: "Tipo 137",
    description: "Assoalho Externo",
    status: "default",
  },
  {
    failType: 7,
    title: "Tipo 140",
    description: "Documentação",
    status: "default",
  },
  {
    failType: 8,
    title: "Tipo 9830945",
    description: "Teste Backoffice",
    status: "default",
  },
  {
    failType: 9,
    title: "Tipo 9830946",
    description: "Elétrica",
    status: "default",
  },
]);
