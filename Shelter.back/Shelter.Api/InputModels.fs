module InputModels

open System.Runtime.Serialization

[<DataContract>]
type GemInputModel =
  { 
    [<field: DataMember(Name = "title")>]
    title : string 
    [<field: DataMember(Name = "text")>]
    text : string 
  }


[<DataContract>]
type TagInputModel =
  { 
    [<field: DataMember(Name = "label")>]
    label : string 
  }

