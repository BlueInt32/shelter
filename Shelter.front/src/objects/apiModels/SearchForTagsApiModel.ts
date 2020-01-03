import { shelterConfig } from '../../shelterConfig';

export class SearchForTagsApiModel {
  public labelSearchText: string;

  constructor(text: string) {
    this.labelSearchText = text;
  }
}
