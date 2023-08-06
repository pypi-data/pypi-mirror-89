class static:
    """
    multisupport all versions of testcanarybot that have "static" version object
    """

main = [0.801, 0.802, 0.9, 0.906]
beta_versions = {
    0.9: [0.85 + 0.001 * i for i in range(1, 9)]
}

beta = []

for i in beta_versions.keys(): beta.extend(beta_versions[i])

supporting = [*main, *beta]
supporting.sort()
supporting = [static, *supporting]

current = supporting[-1]