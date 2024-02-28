import * as postgres from "https://deno.land/x/postgres@v0.14.2/mod.ts";
import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
const databaseUrl = Deno.env.get("SUPABASE_DB_URL")!;
const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

serve(async (_req: Request) => {
  if (_req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }
  try {
    // Example of how to get query parameters passed to the function
    const { exampleParameter } = await _req.json();
    querySqlExample();
    querySupabaseUserExample(_req.headers.get("Authorization"));
    querySupabaseServiceExample();

    const responseString = JSON.stringify({
      message: `Example function ran successfully with parameter: ${exampleParameter}`,
    });
    return new Response(responseString, {
      status: 200,
      headers: {
        ...corsHeaders,
        "Content-Type": "application/json; charset=utf-8",
      },
    });
  } catch (error) {
    console.error(error);
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
      status: 400,
    });
  }
});

// Example DB query using SQL
async function querySqlExample() {
  const pool = new postgres.Pool(databaseUrl, 3, true);
  const client = await pool.connect();
  const result = await client.queryObject("SELECT * FROM profiles");
  client.release();
  return result.rows;
}

// Example Supabase query with user level permissions
async function querySupabaseUserExample(authorizationHeader: any) {
  const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    global: { headers: { Authorization: authorizationHeader } },
  });
  const { data } = await supabase.from("profiles").select("*").throwOnError();
  return data;
}

// Example Supabase query with service role permissions
async function querySupabaseServiceExample() {
  const supabase = createClient(supabaseUrl, supabaseServiceKey);
  const { data } = await supabase.from("profiles").select("*").throwOnError();
  return data;
}
