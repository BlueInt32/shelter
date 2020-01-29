import { Element } from './Element';
import { Tag } from './Tag';

export interface RootState {
  version: string;
  posts: Element[];
  tags: Tag[];
}
