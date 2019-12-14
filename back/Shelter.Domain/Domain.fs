namespace Shelter.Domain

open System
open System.Runtime.Serialization

type FileType = Image | Video 
type FileData = {
    Extension: string;
    ThumbWidth: int;
    ThumbHeight: int;}

type Tag = { 
    Id:int; 
    Label:string; }

[<DataContract>]
type [<CLIMutable>] Gem =
    {
        [<field: DataMember(Name = "id")>]
        Id: int
        [<field: DataMember(Name = "title")>]
        Title: string
        [<field: DataMember(Name = "text")>]
        Text: string
        [<field: DataMember(Name = "creationDate")>]
        CreationDate: DateTime
        [<field: DataMember(Name = "lastUpdateDate")>]
        LastUpdateDate: DateTime
    }
    
//[<DataContract>]
//type Gem = { 
//    [<field: DataMember(Name = "id")>]
//    Id:int64; 
//    [<field: DataMember(Name = "title")>]
//    Title: Option<string>;
//    [<field: DataMember(Name = "text")>]
//    Text: Option<string>;
//    //FileType: FileType;
//    //FileData: FileData;
//    [<field: DataMember(Name = "creationDate")>]
//    CreationDate: DateTime;
//    //LastUpdateDate: DateTime;
//    //Tags: Option<Tag[]>;
//    }

module Say =
    let hello name =
        printfn "Hello %s" name


/// Dummy types for prototyping
[<DataContract>]
type Foo =
  { [<field: DataMember(Name = "foo")>]
    foo : string }

[<DataContract>]
type Bar =
  { [<field: DataMember(Name = "bar")>]
    bar : string }
