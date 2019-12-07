import { PatchDescriptorModel } from './PatchDescriptorModel';
import { nameofFactory } from '../../services/utils';

const nameof = nameofFactory<GemSaveApiModel>();

export class GemSaveApiModel {
  public id?: number;
  public type: string;
  public title: string;
  public source: string;
  public moreDetails: string;
  public tagsIds: number[];
  public fileUrl: string;
  public base64File: string;
  public mimeType: string;

  constructor() {
    this.type = '';
    this.title = '';
    this.source = '';
    this.moreDetails = '';
    this.tagsIds = [];
    this.fileUrl = '';
    this.base64File = '';
    this.mimeType = '';
  }

  public buildPatchModel(): Array<PatchDescriptorModel<any>> {
    return [
      new PatchDescriptorModel<string>(nameof('title'), this.title),
      new PatchDescriptorModel<string>(nameof('source'), this.source),
      new PatchDescriptorModel<string>(nameof('moreDetails'), this.moreDetails),
      new PatchDescriptorModel<Array<number>>(nameof('tagsIds'), this.tagsIds),
      new PatchDescriptorModel<string>(nameof('fileUrl'), this.fileUrl),
      new PatchDescriptorModel<string>(nameof('base64File'), this.base64File),
      new PatchDescriptorModel<string>(nameof('mimeType'), this.mimeType)
    ];
  }
}
