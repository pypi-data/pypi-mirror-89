import click
from mush_lang.mush_lang import load, repl as mu_repl

banner = '''
               |       |                   
,-.-..   .,---.|---.   |    ,---.,---.,---.
| | ||   |`---.|   |---|    ,---||   ||   |
` ' '`---'`---'`   '   `---'`---^`   '`---|
                                      `---'
> Think and work in the future, not the present or past. – Alan Kay
mush-lang 0.0.1
Powered by CodeLab\n
'''

# todo adapter ip

@click.command()
@click.argument('script', required=False)
def main(script):  # replace
    '''
    mush-lang
    '''
    if script:
        load(script)
    else:
        print(banner)
        mu_repl()
