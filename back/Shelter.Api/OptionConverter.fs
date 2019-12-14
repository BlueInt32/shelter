module Api

open System
open System.Text
open Microsoft.FSharp.Reflection
open Newtonsoft.Json
open Newtonsoft.Json.Converters
open Suave
open Suave
open Suave
open Newtonsoft.Json.Serialization
open Newtonsoft.Json
open Newtonsoft.Json.Serialization
open Suave
open Suave.Operators
open Suave.Http
open Suave.Successful


type OptionConverter() =
    inherit JsonConverter()

    override x.CanConvert(t) = 
        t.IsGenericType && t.GetGenericTypeDefinition() = typedefof<option<_>>

    override x.WriteJson(writer, value, serializer) =
        let value = 
            if value = null then null
            else 
                let _,fields = FSharpValue.GetUnionFields(value, value.GetType())
                fields.[0]  
        serializer.Serialize(writer, value)

    override x.ReadJson(reader, t, existingValue, serializer) =        
        let innerType = t.GetGenericArguments().[0]
        let innerType = 
            if innerType.IsValueType then (typedefof<Nullable<_>>).MakeGenericType([|innerType|])
            else innerType        
        let value = serializer.Deserialize(reader, innerType)
        let cases = FSharpType.GetUnionCases(t)
        if value = null then FSharpValue.MakeUnion(cases.[0], [||])
        else FSharpValue.MakeUnion(cases.[1], [|value|])

let jsonSerializerSettings = new JsonSerializerSettings()
jsonSerializerSettings.Converters.Add(new OptionConverter())
jsonSerializerSettings.NullValueHandling <- NullValueHandling.Ignore

let toJsonBytes output = 
    let stringResult = JsonConvert.SerializeObject(output,jsonSerializerSettings)
    Encoding.UTF8.GetBytes(stringResult)
    
let toJson output = 
    JsonConvert.SerializeObject(output,jsonSerializerSettings)
    
let fromJson<'a> json =
  JsonConvert.DeserializeObject(json, typeof<'a>) :?> 'a

let getResourceFromReq<'a> (req : HttpRequest) =
  let getString (rawForm:byte[]) =
    System.Text.Encoding.UTF8.GetString(rawForm)
  req.rawForm |> getString |> fromJson<'a>

let JSON v =
  let jsonSerializerSettings = new JsonSerializerSettings()
  jsonSerializerSettings.ContractResolver <- new CamelCasePropertyNamesContractResolver()

  JsonConvert.SerializeObject(v, jsonSerializerSettings)
  |> OK
  >=> Writers.setMimeType "application/json; charset=utf-8"
