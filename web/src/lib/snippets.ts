import { MCP_URL } from './api';

export interface CodeLanguage {
	id: string;
	label: string;
}

export const CODE_LANGUAGES: CodeLanguage[] = [
	{ id: 'curl', label: 'cURL' },
	{ id: 'js', label: 'JavaScript' },
	{ id: 'python', label: 'Python' },
	{ id: 'go', label: 'Go' },
	{ id: 'php', label: 'PHP' },
	{ id: 'ruby', label: 'Ruby' },
	{ id: 'dart', label: 'Dart' }
];

/** Code that sends one GET request and reads the `data` field of the answer. */
export function codeFor(language: string, url: string): string {
	switch (language) {
		case 'js':
			return `const response = await fetch('${url}');
if (!response.ok) throw new Error(\`HTTP \${response.status}\`);
const { data } = await response.json();

console.log(data);`;
		case 'python':
			return `import requests

response = requests.get("${url}", timeout=10)
response.raise_for_status()
data = response.json()["data"]

print(data)`;
		case 'go':
			return `resp, err := http.Get("${url}")
if err != nil {
	log.Fatal(err)
}
defer resp.Body.Close()

var result struct {
	Data json.RawMessage \`json:"data"\`
}
if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
	log.Fatal(err)
}
fmt.Println(string(result.Data))`;
		case 'php':
			return `$body = file_get_contents('${url}');
$data = json_decode($body, true)['data'];

print_r($data);`;
		case 'ruby':
			return `require 'net/http'
require 'json'

body = Net::HTTP.get(URI('${url}'))
data = JSON.parse(body)['data']

puts data`;
		case 'dart':
			return `import 'dart:convert';
import 'package:http/http.dart' as http;

final response = await http.get(Uri.parse('${url}'));
final data = jsonDecode(response.body)['data'];

print(data);`;
		default:
			return `curl "${url}"`;
	}
}

export interface McpClient {
	id: 'claude-code' | 'claude-desktop' | 'cursor' | 'vscode' | 'stdio' | 'local';
	/** Product names are not translated; the last two get a label from the dictionary. */
	label: string;
	lang: 'bash' | 'json' | 'text';
	code: string;
}

export const MCP_CLIENTS: McpClient[] = [
	{ id: 'claude-code', label: 'Claude Code', lang: 'bash', code: `claude mcp add --transport http bmkg ${MCP_URL}` },
	{ id: 'claude-desktop', label: 'Claude Desktop', lang: 'text', code: MCP_URL },
	{
		id: 'cursor',
		label: 'Cursor',
		lang: 'json',
		code: `{
  "mcpServers": {
    "bmkg": {
      "url": "${MCP_URL}"
    }
  }
}`
	},
	{ id: 'vscode', label: 'VS Code', lang: 'bash', code: `code --add-mcp '{"name":"bmkg","type":"http","url":"${MCP_URL}"}'` },
	{
		id: 'stdio',
		label: '',
		lang: 'json',
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
		label: '',
		lang: 'json',
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

export const MCP_TOOLS: { name: string; args: string }[] = [
	{ name: 'get_latest_earthquake', args: '' },
	{ name: 'get_recent_earthquakes', args: '' },
	{ name: 'get_felt_earthquakes', args: '' },
	{ name: 'get_nearby_earthquakes', args: 'latitude, longitude, radius_km' },
	{ name: 'get_weather_forecast', args: 'adm4_code' },
	{ name: 'get_current_weather', args: 'adm4_code' },
	{ name: 'get_weather_warnings', args: 'language' },
	{ name: 'check_location_warnings', args: 'location, language' },
	{ name: 'search_regions', args: 'query, limit' },
	{ name: 'get_provinces', args: '' },
	{ name: 'get_districts', args: 'province_code' },
	{ name: 'get_subdistricts', args: 'district_code' },
	{ name: 'get_villages', args: 'subdistrict_code' }
];

/** Real questions the tools can answer, in the language users ask them. */
export const MCP_PROMPTS = [
	'Gempa terbaru di Indonesia?',
	'Cuaca 3 hari ke depan di Jakarta Selatan?',
	'Ada peringatan cuaca di Yogyakarta?'
];
