import { shelterConfig } from '../../shelterConfig';

export class SearchForGemsApiModel {
  public pageSize: number;
  public startIndex: number;
  public sortingProperty: string;
  public sortingDirection: string;
  public tagsIds: number[];
  public hiddenTagsIds: number[];

  constructor() {
    this.pageSize = shelterConfig.defaultPageSize;
    this.startIndex = 0;
    this.sortingProperty = 'creationDate';
    this.sortingDirection = 'descending';
    this.tagsIds = [];
    this.hiddenTagsIds = [];
  }
}
