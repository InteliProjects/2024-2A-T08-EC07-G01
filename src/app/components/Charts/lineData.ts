// assets/linedata.ts

import axios from "axios";

// Interface para os dados de cada mês
export interface FailCodeCount {
  [month: string]: number;
}

export interface LineChartApiResponse {
  predicted_fail_code_count: FailCodeCount;
  real_fail_code_count: FailCodeCount;
}

export interface MonthData {
  name: string;
  Predito: number;
  Real: number;
}

export type LineChartData = MonthData[];

/**
 * Função para buscar os dados do gráfico a partir da API.
 * @param failCode Número da classe de falhas selecionada.
 * @param year Ano para o qual os dados devem ser buscados.
 * @returns Promessa que resolve para os dados formatados para o gráfico.
 */
export async function fetchChartData(failCode: number, year: number = new Date().getFullYear()): Promise<LineChartData> {

  const config = useRuntimeConfig();
  const apiURL = config.public.backendUrl;

  const baseURL = `${apiURL}/api/predictions`;

  try {
    const response = await axios.post<LineChartApiResponse>(`${baseURL}/fail-codes-by-month`, {
      year: year,
      fail_code: failCode,
    });

    const { predicted_fail_code_count, real_fail_code_count } = response.data;

    // Lista dos meses no formato esperado (em lowercase)
    const months = [
      "january", "february", "march", "april", "may", "june",
      "july", "august", "september", "october", "november", "december"
    ];

    // Função auxiliar para capitalizar a primeira letra
    const capitalizeFirstLetter = (str: string): string => {
      if (!str) return '';
      return str.charAt(0).toUpperCase() + str.slice(1);
    };

    // Mapeia os dados para o formato esperado pelo LineChart
    const chartData: LineChartData = months.map(month => ({
      name: capitalizeFirstLetter(month),
      Predito: predicted_fail_code_count[month] || 0,
      Real: real_fail_code_count[month] || 0,
    }));

    return chartData;
  } catch (error) {
    console.error("Error fetching data:", error);
    return []; // Retorna um array vazio em caso de erro
  }
}
