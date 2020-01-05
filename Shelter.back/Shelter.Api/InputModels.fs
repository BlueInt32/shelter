module InputModels

open System.Runtime.Serialization


[<DataContract>]
type TagInputModel =
  { 
    [<field: DataMember(Name = "label")>]
    label : string 
  }

[<DataContract>]
type GemInputModel =
  { 
    [<field: DataMember(Name = "title")>]
    title : string 
    [<field: DataMember(Name = "text")>]
    text : string 
    [<field: DataMember(Name = "tags")>]
    tags :string[]
  }

[<DataContract>]
type TagsSearchInputModel = 
    {
        [<field: DataMember(Name = "labelSearchText")>]
        labelSearchText : string 

        [<field: DataMember(Name = "limit")>]
        limit : int 
    }

