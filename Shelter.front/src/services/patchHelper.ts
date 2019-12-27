export let buildPatchModifierPayload = (propPath: string, value: string) => ({
  op: 'replace',
  path: `/${propPath}`,
  value
});
