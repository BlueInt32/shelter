namespace Shed.Domain

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
type Gem() =  
    [<field: DataMember(Name = "id")>]
    member val Id:int64 = 0L with get, set 
    [<field: DataMember(Name = "title")>]
    member val Title:string = String.Empty with get, set 
    [<field: DataMember(Name = "text")>]
    member val Text:string = String.Empty with get, set 
    //FileType: FileType;
    //FileData: FileData;
    [<field: DataMember(Name = "creationDate")>]
    member val CreationDate: Option<DateTime> = None with get, set 
    //LastUpdateDate: DateTime;
    //Tags: Option<Tag[]>;
    

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
