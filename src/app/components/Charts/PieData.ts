import axios from "axios";

export interface TestPieChart {
  name: string;
  total: number;
  predicted: number;
}

export async function fetchChartData(isFromFails: boolean): Promise<TestPieChart[]> {
  const config = useRuntimeConfig();
  const apiURL = config.public.backendUrl;

  const baseURL = `${apiURL}/api/predictions`;

  try {
    let response;
    if (isFromFails) {
      response = await axios.get(`${baseURL}/total-fails`);
      const responseData = response.data;

      return [
        { name: "Sem Falha", total: responseData.no_fails, predicted: 0 },
        { name: "Com Falha", total: responseData.fails, predicted: 0 },
      ];
    } else {
      response = await axios.get(`${baseURL}/fail-codes-predicted`);
      const responseData = response.data;

      return Object.keys(responseData)
      .filter((key) => key != "0")
      .map((key) => ({
        name: `Falha ${key}`,
        total: responseData[key],
        predicted: 0,
      }));
  }
  } catch (error) {
    console.error("Error fetching data:", error);
    return []; // Reset to empty if there's an error
  }
}
