module HttpUtilities
open Suave.Operators
open Suave.Writers
open Suave.Filters
open Suave.Json

let setCORSHeaders =
    setHeader "Access-Control-Allow-Origin" "*"
    >=> setHeader "Access-Control-Allow-Headers" "content-type"

let POST_CORS = POST >=> setCORSHeaders

let mapJsonSbu f = mapJsonWith fromJson Api.toJsonBytes f
