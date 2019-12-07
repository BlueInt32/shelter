export class PatchDescriptorModel<T> {
  public op: string;
  public path: string;
  public value: T;

  constructor(path: string, value: T) {
    this.op = 'replace';
    this.path = `/${path}`;
    this.value = value;
  }
}
