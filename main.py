import xml.etree.ElementTree as ET
import requests
import os


def load_pom(file_path):
    """
    Carrega o arquivo POM XML e retorna a árvore e a raiz do XML.

    Args:
        file_path (str): Caminho para o arquivo POM.

    Returns:
        tuple: Árvore e raiz do XML, ou (None, None) em caso de erro.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return tree, root
    except ET.ParseError:
        print("Erro ao carregar o arquivo XML.")
        return None, None


def extract_dependencies(root):
    """
    Extrai as dependências do arquivo POM.

    Args:
        root (Element): Raiz do XML do POM.

    Returns:
        list: Lista de tuplas contendo group_id, artifact_id e versão das dependências.
    """
    namespaces = {'maven': 'http://maven.apache.org/POM/4.0.0'}
    dependencies = []
    for dep in root.findall(".//maven:dependency", namespaces):
        group_id = dep.find("maven:groupId", namespaces).text if dep.find(
            "maven:groupId", namespaces) else None
        artifact_id = dep.find("maven:artifactId", namespaces).text if dep.find(
            "maven:artifactId", namespaces) else None
        version = dep.find("maven:version", namespaces).text if dep.find(
            "maven:version", namespaces) else "unknown"

        if group_id and artifact_id:
            dependencies.append((group_id, artifact_id, version))

    return dependencies


def get_latest_version(group_id, artifact_id):
    """
    Obtém a versão mais recente de uma dependência do Maven Central.

    Args:
        group_id (str): Group ID da dependência.
        artifact_id (str): Artifact ID da dependência.

    Returns:
        str: Última versão da dependência, ou None em caso de erro.
    """
    group_id_path = group_id.replace('.', '/')
    url = f"https://repo1.maven.org/maven2/{group_id_path}/{artifact_id}/maven-metadata.xml"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            metadata = ET.fromstring(response.content)
            latest_version = metadata.find("./versioning/latest").text
            return latest_version
        except Exception as e:
            print(f"Erro ao processar XML para {artifact_id}: {e}")
    else:
        print(
            f"Não foi possível obter a versão mais recente para {artifact_id}")

    return None


def update_pom_with_new_versions(tree, root, dependencies):
    """
    Atualiza o arquivo POM com as versões mais recentes das dependências.

    Args:
        tree (ElementTree): Árvore do XML do POM.
        root (Element): Raiz do XML do POM.
        dependencies (list): Lista de dependências extraídas do POM.
    """
    namespaces = {'maven': 'http://maven.apache.org/POM/4.0.0'}
    dep_elements = root.findall(".//maven:dependency", namespaces)

    for dep in dep_elements:
        group_id = dep.find("maven:groupId", namespaces).text
        artifact_id = dep.find("maven:artifactId", namespaces).text

        latest_version = get_latest_version(group_id, artifact_id)
        if latest_version:
            dep.find("maven:version", namespaces).text = latest_version

    tree.write("updated_pom.xml", encoding="utf-8", xml_declaration=True)
    print("Arquivo 'updated_pom.xml' gerado com sucesso!")


if __name__ == "__main__":
    file_path = "pom.xml"
    tree, root = load_pom(file_path)

    if root:
        dependencies = extract_dependencies(root)
        update_pom_with_new_versions(tree, root, dependencies)
