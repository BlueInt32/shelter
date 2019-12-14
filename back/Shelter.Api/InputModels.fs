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

