import { MCP_URL, PUBLIC_ORIGIN } from './api';

const url = `${PUBLIC_ORIGIN}/v1/earthquake/latest`;

export interface Snippet {
	id: string;
	label: string;
	code: string;
}

export const CODE_SAMPLES: Snippet[] = [
	{ id: 'curl', label: 'cURL', code: `curl ${url}` },
	{
		id: 'js',
		label: 'JavaScript',
		code: `const response = await fetch('${url}');
const { data } = await response.json();

console.log(\`M \${data.magnitude} · \${data.region}\`);`
	},
	{
		id: 'python',
		label: 'Python',
		code: `import requests

data = requests.get("${url}", timeout=10).json()["data"]

print(f"M {data['magnitude']} · {data['region']}")`
	},
	{
		id: 'go',
		label: 'Go',
		code: `resp, err := http.Get("${url}")
if err != nil {
	log.Fatal(err)
}
defer resp.Body.Close()

var result struct {
	Data struct {
		Magnitude float64 \`json:"magnitude"\`
		Region    string  \`json:"region"\`
	} \`json:"data"\`
}
json.NewDecoder(resp.Body).Decode(&result)
fmt.Printf("M %.1f · %s\\n", result.Data.Magnitude, result.Data.Region)`
	},
	{
		id: 'php',
		label: 'PHP',
		code: `$result = json_decode(file_get_contents('${url}'), true);
$data = $result['data'];

echo "M {$data['magnitude']} · {$data['region']}";`
	},
	{
		id: 'ruby',
		label: 'Ruby',
		code: `require 'net/http'
require 'json'

data = JSON.parse(Net::HTTP.get(URI('${url}')))['data']

puts "M #{data['magnitude']} · #{data['region']}"`
	},
	{
		id: 'dart',
		label: 'Dart',
		code: `import 'dart:convert';
import 'package:http/http.dart' as http;

final response = await http.get(Uri.parse('${url}'));
final data = jsonDecode(response.body)['data'];

print('M \${data['magnitude']} · \${data['region']}');`
	}
];

export const MCP_CLIENTS: (Snippet & { note: string; lang: 'bash' | 'json' })[] = [
	{
		id: 'claude-code',
		label: 'Claude Code',
		lang: 'bash',
		note: 'One command. Or install the plugin: claude plugin marketplace add dhanyyudi/bmkg-api, then claude plugin install bmkg@bmkg-api.',
		code: `claude mcp add --transport http bmkg ${MCP_URL}`
	},
	{
		id: 'claude-desktop',
		label: 'Claude Desktop',
		lang: 'bash',
		note: 'Settings → Connectors → Add custom connector, then paste this URL. Works on claude.ai too.',
		code: MCP_URL
	},
	{
		id: 'cursor',
		label: 'Cursor',
		lang: 'json',
		note: 'Add to ~/.cursor/mcp.json.',
		code: `{
  "mcpServers": {
    "bmkg": {
      "url": "${MCP_URL}"
    }
  }
}`
	},
	{
		id: 'vscode',
		label: 'VS Code',
		lang: 'bash',
		note: 'Adds the server to your user profile.',
		code: `code --add-mcp '{"name":"bmkg","type":"http","url":"${MCP_URL}"}'`
	},
	{
		id: 'stdio',
		label: 'Other clients',
		lang: 'json',
		note: 'For clients that only speak stdio: bridge to the hosted server with mcp-remote.',
		code: `{
  "mcpServers": {
    "bmkg": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "${MCP_URL}"]
    }
  }
}`
	},
	{
		id: 'local',
		label: 'Run locally',
		lang: 'json',
		note: 'Runs the server on your machine with uv. Needs Python 3.12 or newer.',
		code: `{
  "mcpServers": {
    "bmkg": {
      "command": "uvx",
      "args": ["bmkg-api-mcp"]
    }
  }
}`
	}
];

export const MCP_TOOLS = [
	{ name: 'get_latest_earthquake', args: '', returns: 'The most recent earthquake' },
	{ name: 'get_recent_earthquakes', args: '', returns: 'The 15 most recent earthquakes of M 5.0+' },
	{ name: 'get_felt_earthquakes', args: '', returns: 'The 15 most recent earthquakes people felt' },
	{ name: 'get_nearby_earthquakes', args: 'latitude, longitude, radius_km', returns: 'Recent earthquakes around a point' },
	{ name: 'get_weather_forecast', args: 'adm4_code', returns: '3-day forecast in 3-hour steps' },
	{ name: 'get_current_weather', args: 'adm4_code', returns: 'Forecast for the current 3-hour slot' },
	{ name: 'get_weather_warnings', args: 'language', returns: 'Active severe weather warnings by province' },
	{ name: 'check_location_warnings', args: 'location, language', returns: 'Active warnings that mention a place' },
	{ name: 'search_regions', args: 'query, limit', returns: 'Regions matching a name, with codes' },
	{ name: 'get_provinces', args: '', returns: 'Provinces with 2-digit codes' },
	{ name: 'get_districts', args: 'province_code', returns: 'Kabupaten and kota of a province' },
	{ name: 'get_subdistricts', args: 'district_code', returns: 'Kecamatan of a district' },
	{ name: 'get_villages', args: 'subdistrict_code', returns: 'Kelurahan and desa, with adm4 codes' }
];
