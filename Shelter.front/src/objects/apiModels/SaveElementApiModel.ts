import { PatchDescriptorModel } from './PatchDescriptorModel';
import { nameofFactory } from '../../services/utils';

const nameof = nameofFactory<SaveElementApiModel>();

export class SaveElementApiModel {
  public id: number | null;
  public title: string;
  public text: string;
  public tags: string[];
  public linkUrl: string;
  // public base64File: string;
  // public mimeType: string;

  constructor() {
    this.id = null;
    this.title = '';
    this.text = '';
    this.tags = [];
    this.linkUrl = '';
    // this.base64File = '';
    // this.mimeType = '';
  }

  public buildPatchModel(): Array<PatchDescriptorModel<any>> {
    return [
      new PatchDescriptorModel<string>(nameof('title'), this.title),
      new PatchDescriptorModel<string>(nameof('text'), this.text),
      new PatchDescriptorModel<Array<string>>(nameof('tags'), this.tags),
      new PatchDescriptorModel<string>(nameof('linkUrl'), this.linkUrl)
      // new PatchDescriptorModel<string>(nameof('base64File'), this.base64File),
      // new PatchDescriptorModel<string>(nameof('mimeType'), this.mimeType)
    ];
  }
}

export class SaveElementWithFileApiModel {
  public json: SaveElementApiModel = new SaveElementApiModel();
  public file: File | null;
  constructor(json: SaveElementApiModel, file: File | null) {
    this.json = json;
    this.file = file;
  }
}
