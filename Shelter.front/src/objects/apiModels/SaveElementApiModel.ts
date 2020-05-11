import { PatchDescriptorModel } from './PatchDescriptorModel';
import { nameofFactory } from '../../services/utils';
import { FileType } from './FileType';

const nameof = nameofFactory<SaveElementApiModel>();

export class SaveElementApiModel {
  public id: number | null;
  public title: string;
  public text: string;
  public tags: string[];
  public linkUrl: string;

  constructor() {
    this.id = null;
    this.title = '';
    this.text = '';
    this.tags = [];
    this.linkUrl = '';
  }

  public buildPatchModel(): Array<PatchDescriptorModel<any>> {
    return [
      new PatchDescriptorModel<string>(nameof('title'), this.title),
      new PatchDescriptorModel<string>(nameof('text'), this.text),
      new PatchDescriptorModel<Array<string>>(nameof('tags'), this.tags),
      new PatchDescriptorModel<string>(nameof('linkUrl'), this.linkUrl)
    ];
  }
}

export class SaveElementWithFileApiModel {
  public json: SaveElementApiModel = new SaveElementApiModel();
  public file: File | null;
  public fileType: FileType;

  constructor(
    json: SaveElementApiModel,
    file: File | null,
    fileType: FileType
  ) {
    this.json = json;
    this.file = file;
    this.fileType = fileType;
  }
}
