from app.models.knr import KNR

fails = {
    0: "Sem falha",
    1: "Parte Traseira",
    2: "Parte Central",
    4: "Portas",
    5: "Parte Dianteira",
    133: "Geral",
    137: "Assoalho Externo",
    140: "Documentação",
    9830945: "Teste Backoffice",
    9830946: "Elétrica",
}


def label_fail(fail_code: int) -> str:
    if fail_code == "":
        return ""

    return fails.get(fail_code, "")


def label_knr(knr: KNR) -> KNR:
    if knr.predicted_fail_codes == [-1] or knr.predicted_fail_codes is None:
        return knr

    knr.predicted_fails = []
    for fail in knr.predicted_fail_codes:
        knr.predicted_fails.append(label_fail(fail))

    if knr.real_fail_codes == [-1] or knr.real_fail_codes is None:
        return knr

    knr.real_fails = []
    for fail in knr.real_fail_codes:
        knr.real_fails.append(label_fail(fail))

    return knr
