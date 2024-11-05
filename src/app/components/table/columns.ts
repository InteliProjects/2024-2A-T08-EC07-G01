import { h } from "vue";
import { ArrowUpDown } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import type { ColumnDef } from "@tanstack/vue-table";

interface TestData {
  knr: string;
  //   dataPrevisao: string;
  falha: string;
  tipoFalha: string;
  testeIndicado: string;
}

export const columns: ColumnDef<TestData>[] = [
  {
    accessorKey: "knr",
    header: ({ column }) => {
      return h(
        Button,
        {
          variant: "ghost",
          onClick: () => column.toggleSorting(column.getIsSorted() === "asc"),
          class: "pl-[2px]", // Adjusted padding-left to move text KNR to the left
        },
        () => ["KNR", h(ArrowUpDown, { class: "ml-2 h-4 w-4" })]
      );
    },
  },
  // {
  //     accessorKey: 'dataPrevisao',
  //     header: ({ column }) => {
  //         return h(Button, {
  //             variant: 'ghost',
  //             onClick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
  //             class: 'pl-[2px]', // Adjusted padding-left to move text to the left
  //         }, () => ['Data de Previsão', h(ArrowUpDown, { class: 'ml-2 h-4 w-4' })])
  //     },
  // },
  {
    accessorKey: "falha",
    header: ({ column }) => {
      return h(
        Button,
        {
          variant: "ghost",
          onClick: () => column.toggleSorting(column.getIsSorted() === "asc"),
          class: "pl-[2px]", // Adjusted padding-left to move text to the left
        },
        () => ["Falha", h(ArrowUpDown, { class: "ml-2 h-4 w-4" })]
      );
    },
  },
  {
    accessorKey: "tipoFalha",
    header: ({ column }) => {
      return h(
        Button,
        {
          variant: "ghost",
          onClick: () => column.toggleSorting(column.getIsSorted() === "asc"),
          class: "pl-[2px]", // Adjusted padding-left to move text to the left
        },
        () => ["Tipo de Falha", h(ArrowUpDown, { class: "ml-2 h-4 w-4" })]
      );
    },
  },
  {
    accessorKey: "testeIndicado",
    header: ({ column }) => {
      return h(
        Button,
        {
          variant: "ghost",
          onClick: () => column.toggleSorting(column.getIsSorted() === "asc"),
          class: "pl-[2px]", // Adjusted padding-left to move text to the left
        },
        () => ["Teste Indicado", h(ArrowUpDown, { class: "ml-2 h-4 w-4" })]
      );
    },
  },
];
