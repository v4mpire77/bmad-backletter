export function anchorTermsFor(detectorId: string): string[] {
  const id = detectorId.toLowerCase();
  if (id.includes("instructions")) return ["documented instructions", "controller's instructions"];
  if (id.includes("confidentiality")) return ["confidentiality", "confidential obligations"];
  if (id.includes("security")) return ["technical and organisational measures", "tom", "security measures"];
  if (id.includes("subprocessors")) return ["sub-processors", "subprocessors", "prior written authorisation"];
  if (id.includes("data_subjects")) return ["data subject requests", "data subjects"];
  if (id.includes("assistance")) return ["assist the controller", "assistance to the controller"];
  if (id.includes("deletion_return")) return ["delete or return", "return all the personal data"];
  if (id.includes("audit")) return ["demonstrate compliance", "allow for audits", "audit"];
  return [];
}

