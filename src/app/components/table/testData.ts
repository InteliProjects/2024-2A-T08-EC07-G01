export interface Prediction {
  KNR: string;
  predicted_fail_codes: number[];
  real_fail_codes: number[];
  indicated_tests: string[];
}

export interface TableData {
  knr: string;
  falha: string;
  tipoFalha: string;
  testeIndicado: string;
}

export const convertPredictionToTableData = (
  predictionData: Prediction[]
): TableData[] => {
  return predictionData.map((prediction) => {
    // Check if there is any non-zero value in predicted_fail_codes
    const hasFailure = prediction.predicted_fail_codes.some(code => code !== 0);

    // Falha column should return "Possui Falha" if any predicted_fail_codes is non-zero
    const falha = hasFailure ? "Possui Falha" : "Sem Falhas";

    // Tipo de Falha is set to "Não Previsto" as no specific type is mentioned
    const tipoFalha = hasFailure ? "Parte Traseira" : "Não Previsto";

    // Teste Indicado always returns "To-Do"
    const testeIndicado = "To-Do";

    return {
      knr: prediction.KNR,
      falha: falha,
      tipoFalha: tipoFalha,
      testeIndicado: testeIndicado
    };
  });
};
