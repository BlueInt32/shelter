import { PatchDescriptorModel } from './PatchDescriptorModel';
import { nameofFactory } from '../../services/utils';
import { ElementType } from './ElementType';

const nameofBase = nameofFactory<SaveElementBaseApiModel>();
const nameofLink = nameofFactory<SaveElementWithLinkApiModel>();

export class SaveElementBaseApiModel {
  public id: number | null;
  public title: string;
  public text: string;
  public tags: string[];
  public type: ElementType;

  constructor() {
    this.id = null;
    this.title = '';
    this.text = '';
    this.tags = [];
    this.type = ElementType.None;
  }

  public buildPatchModel(): Array<PatchDescriptorModel<any>> {
    return [
      new PatchDescriptorModel<string>(nameofBase('title'), this.title),
      new PatchDescriptorModel<string>(nameofBase('text'), this.text),
      new PatchDescriptorModel<Array<string>>(nameofBase('tags'), this.tags)
    ];
  }
}

export class SaveElementWithFileApiModel extends SaveElementBaseApiModel {
  public file: File | null;

  constructor(file: File | null) {
    super();
    this.file = file;
  }
}

export class SaveElementWithLinkApiModel extends SaveElementBaseApiModel {
  public linkUrl: string;

  constructor(linkUrl: string) {
    super();
    this.linkUrl = linkUrl;
  }

  buildPatchModel(): Array<PatchDescriptorModel<any>> {
    let model = super.buildPatchModel();
    model.push(
      new PatchDescriptorModel<string>(nameofLink('linkUrl'), this.linkUrl)
    );
    return model;
  }
}
