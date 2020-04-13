import { Tag } from './Tag';

export class Element {
  constructor() {
    this.id = 0;
    this.title = '';
    this.text = '';
    this.tags = [];
    this.fileUrl = '';
    this.thumbnailUrl = '';
    this.creation_date = '';
  }

  public id: number;
  public title: string;
  public text: string;
  public tags: Tag[];
  public fileUrl: string;
  public thumbnailUrl: string;
  public creation_date: string;
}
