const createClientMock = jest.fn(() => ({}));
jest.mock('@supabase/supabase-js', () => ({ createClient: createClientMock }));

describe('supabaseClient', () => {
  beforeEach(() => {
    delete process.env.NEXT_PUBLIC_SUPABASE_URL;
    delete process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    jest.resetModules();
    createClientMock.mockClear();
  });

  it('throws when env vars are missing', () => {
    const warnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
    expect(() => require('@/lib/supabaseClient')).toThrow(
      /NEXT_PUBLIC_SUPABASE_URL|NEXT_PUBLIC_SUPABASE_ANON_KEY/
    );
    expect(warnSpy).toHaveBeenCalled();
    warnSpy.mockRestore();
  });

  it('creates client when env vars are present', () => {
    process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://example.supabase.co';
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'anon';
    const { supabase } = require('@/lib/supabaseClient');
    expect(createClientMock).toHaveBeenCalledWith(
      'https://example.supabase.co',
      'anon'
    );
    expect(supabase).toBeDefined();
  });
});
