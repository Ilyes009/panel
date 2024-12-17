// Temporary mock implementation since we'll call the Python backend instead
export class api {
  constructor(
    public name: string,
    public ownerid: string,
    public version: string,
    public hash_to_check: string
  ) {}

  async init() {
    // Implementation will be handled by backend
    return true;
  }

  async license(key: string) {
    const response = await fetch('/auth/validate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ key })
    });
    
    if (!response.ok) {
      throw new Error('Invalid license key');
    }
    
    return await response.json();
  }
}