module Db

open System
open System.Collections.Generic
open System.Data.SQLite
open Shed.Domain
open System.Data

// https://github.com/mausch/FsSql  //
let databaseFilename = __SOURCE_DIRECTORY__ + @"\..\shelter.db"
let connectionStringFile = sprintf "Data Source=%s;Version=3;New=False;Compress=True;" databaseFilename  

// type Person = { Name : string; Age : int }
let openConnection() = 
    let conn = new System.Data.SQLite.SQLiteConnection(connectionStringFile) 
    conn.Open() 
    conn :> IDbConnection 

let connMgr = Sql.withNewConnection openConnection 
let execScalar sql = Sql.execScalar connMgr sql 
let execReader sql = Sql.execReader connMgr sql 
let execReaderf sql = Sql.execReaderF connMgr sql 
let execNonQueryf sql = Sql.execNonQueryF connMgr sql 
let execNonQuery sql p = Sql.execNonQuery connMgr sql p |> ignore 
let exec sql = execNonQuery sql []
let P = Sql.Parameter.make

let getPostsNumber (): int64 = 
    // let filteredSql = "select * From Posts " 
    execScalar "select count(*) from gems" [] |> Option.get 

let getGems () = 
    execReader "select * from gems" [] 
    |> Seq.ofDataReader
    |> Seq.map (fun dr -> 
    // |> Seq.iter (fun dr -> 
        let id = (dr?Id).Value 
        let title = dr?Title 
        let text = dr?Text 
        let creationDate = dr?CreationDate
        // printfn "Id: ?; Name: %s; Address: %s" name creationDate)
        let result = new Gem()
        result.Id <- id
        result.Title <- title
        result.Text <- text
        result.CreationDate <- creationDate
        // { Id=id; Title= title; Text = text; CreationDate= creationDate; }
        result
        )

let createGem (title:string) (text:string) = 
    let creationDate = DateTime.Now
    let lastUpdateDate = DateTime.Now

    execNonQuery "insert into Gems (title, text, creationDate, lastUpdateDate) values (@title, @text, @creationDate, @lastUpdateDate)"
                [P("@title", title); P("@text", text); P("@creationDate", DateTime.Now); P("@lastUpdateDate", DateTime.Now  )] 

    let id = execScalar "select seq from sqlite_sequence where name='Gems'" [] |> Option.get

    let result = new Gem()
    result
    //{ Id=id; Title= Some title; Text = Some text; CreationDate= creationDate; }
