import { Gem } from './Gem';
import { Tag } from './Tag';

export interface RootState {
  version: string;
  posts: Gem[];
  tags: Tag[];
}
