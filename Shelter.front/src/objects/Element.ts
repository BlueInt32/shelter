import { Tag } from './Tag';

export class Element {
  constructor() {
    this.id = 0;
    this.title = '';
    this.text = '';
    this.tags = [];
  }

  public id: number;
  public title: string;
  public text: string;
  public tags: Tag[];
}
