from models import db, Element, Tag

def resolve_tags(input_tags_labels):
  # 1. find tags that are already in db
  (known_tags_labels_set, known_tags) = resolve_known_tags_labels_as_set(input_tags_labels)

  # 2. build Tag instances of tags that need to be created in db
  received_tags_set = set(input_tags_labels or [])
  tags_to_create = [Tag(t) for t in (received_tags_set - known_tags_labels_set)]

  # 3. merge the 2 lists
  output_tags_list = list(set(tags_to_create) | set(known_tags))

  return output_tags_list

def resolve_known_tags_labels_as_set(input_tags_labels):
  # 1. find tags in db that are not in input list
  known_tags = Tag.query.filter(Tag.label.in_(input_tags_labels or [])).all()
  # 2. create a set with their labels
  known_tags_labels_set = set(map(lambda t: t.label, known_tags))
  return (known_tags_labels_set, known_tags)
