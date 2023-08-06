import time
import numpy as np
import pandas as pd
from pegasusio import MultimodalData
from natsort import natsorted

from sklearn.cluster import KMeans
from typing import List, Optional

from pegasus.tools import construct_graph

import logging
logger = logging.getLogger(__name__)

from pegasusio import timer


@timer(logger=logger)
def louvain(
    data: MultimodalData,
    rep: str = "pca",
    resolution: int = 1.3,
    random_state: int = 0,
    class_label: str = "louvain_labels",
) -> None:
    """Cluster the cells using Louvain algorithm. [Blondel08]_

    Parameters
    ----------
    data: ``pegasusio.MultimodalData``
        Annotated data matrix with rows for cells and columns for genes.

    rep: ``str``, optional, default: ``"pca"``
        The embedding representation used for clustering. Keyword ``'X_' + rep`` must exist in ``data.obsm`` and nearest neighbors must be calculated so that affinity matrix ``'W_' + rep`` exists in ``data.uns``. By default, use PCA coordinates.

    resolution: ``int``, optional, default: ``1.3``
        Resolution factor. Higher resolution tends to find more clusters with smaller sizes.

    random_state: ``int``, optional, default: ``0``
        Random seed for reproducing results.

    class_label: ``str``, optional, default: ``"louvain_labels"``
        Key name for storing cluster labels in ``data.obs``.

    Returns
    -------
    ``None``

    Update ``data.obs``:
        * ``data.obs[class_label]``: Cluster labels of cells as categorical data.

    Examples
    --------
    >>> pg.louvain(data)
    """

    try:
        import louvain as louvain_module
    except ImportError:
        print("Need louvain! Try 'pip install louvain-github'.")

    rep_key = "W_" + rep
    if rep_key not in data.uns:
        raise ValueError("Cannot find affinity matrix. Please run neighbors first!")
    W = data.uns[rep_key]

    G = construct_graph(W)
    partition_type = louvain_module.RBConfigurationVertexPartition
    partition = partition_type(G, resolution_parameter=resolution, weights="weight")
    optimiser = louvain_module.Optimiser()
    optimiser.set_rng_seed(random_state)
    diff = optimiser.optimise_partition(partition)

    labels = np.array([str(x + 1) for x in partition.membership])
    categories = natsorted(np.unique(labels))
    data.obs[class_label] = pd.Categorical(values=labels, categories=categories)

    n_clusters = data.obs[class_label].cat.categories.size
    logger.info(f"Louvain clustering is done. Get {n_clusters} clusters.")


@timer(logger=logger)
def leiden(
    data: MultimodalData,
    rep: str = "pca",
    resolution: int = 1.3,
    n_iter: int = -1,
    random_state: int = 0,
    class_label: str = "leiden_labels",
) -> None:
    """Cluster the data using Leiden algorithm. [Traag19]_

    Parameters
    ----------
    data: ``pegasusio.MultimodalData``
        Annotated data matrix with rows for cells and columns for genes.

    rep: ``str``, optional, default: ``"pca"``
        The embedding representation used for clustering. Keyword ``'X_' + rep`` must exist in ``data.obsm`` and nearest neighbors must be calculated so that affinity matrix ``'W_' + rep`` exists in ``data.uns``. By default, use PCA coordinates.

    resolution: ``int``, optional, default: ``1.3``
        Resolution factor. Higher resolution tends to find more clusters.

    n_iter: ``int``, optional, default: ``-1``
        Number of iterations that Leiden algorithm runs. If ``-1``, run the algorithm until reaching its optimal clustering.

    random_state: ``int``, optional, default: ``0``
        Random seed for reproducing results.

    class_label: ``str``, optional, default: ``"leiden_labels"``
        Key name for storing cluster labels in ``data.obs``.

    Returns
    -------
    ``None``

    Update ``data.obs``:
        * ``data.obs[class_label]``: Cluster labels of cells as categorical data.

    Examples
    --------
    >>> pg.leiden(data)
    """

    try:
        import leidenalg
    except ImportError:
        print("Need leidenalg! Try 'pip install leidenalg'.")

    rep_key = "W_" + rep
    if rep_key not in data.uns:
        raise ValueError("Cannot find affinity matrix. Please run neighbors first!")
    W = data.uns[rep_key]

    G = construct_graph(W)
    partition_type = leidenalg.RBConfigurationVertexPartition
    partition = leidenalg.find_partition(
        G,
        partition_type,
        seed=random_state,
        weights="weight",
        resolution_parameter=resolution,
        n_iterations=n_iter,
    )

    labels = np.array([str(x + 1) for x in partition.membership])
    categories = natsorted(np.unique(labels))
    data.obs[class_label] = pd.Categorical(values=labels, categories=categories)

    n_clusters = data.obs[class_label].cat.categories.size
    logger.info(f"Leiden clustering is done. Get {n_clusters} clusters.")


def partition_cells_by_kmeans(
    X: np.ndarray,
    n_clusters: int,
    n_clusters2: int,
    n_init: int,
    random_state: int,
    min_avg_cells_per_final_cluster: Optional[int] = 10,
) -> List[int]:

    n_clusters = min(n_clusters, max(X.shape[0] // min_avg_cells_per_final_cluster, 1))
    if n_clusters == 1:
        return np.zeros(X.shape[0], dtype = np.int32)

    kmeans_params = {
        'n_clusters': n_clusters,
        'n_init': n_init,
        'random_state': random_state,
    }

    km = KMeans(**kmeans_params)
    km.fit(X)
    coarse = km.labels_.copy()

    km.set_params(n_init=1)
    labels = coarse.copy()
    base_sum = 0
    for i in range(n_clusters):
        idx = coarse == i
        nc = min(n_clusters2, max(idx.sum() // min_avg_cells_per_final_cluster, 1))
        if nc == 1:
            labels[idx] = base_sum
        else:
            km.set_params(n_clusters=nc)
            km.fit(X[idx, :])
            labels[idx] = base_sum + km.labels_
        base_sum += nc

    return labels


@timer(logger=logger)
def spectral_louvain(
    data: MultimodalData,
    rep: str = "pca",
    resolution: float = 1.3,
    rep_kmeans: str = "diffmap",
    n_clusters: int = 30,
    n_clusters2: int = 50,
    n_init: int = 10,
    random_state: int = 0,
    class_label: str = "spectral_louvain_labels",
) -> None:
    """ Cluster the data using Spectral Louvain algorithm. [Li20]_

    Parameters
    ----------
    data: ``pegasusio.MultimodalData``
        Annotated data matrix with rows for cells and columns for genes.

    rep: ``str``, optional, default: ``"pca"``
        The embedding representation used for clustering. Keyword ``'X_' + rep`` must exist in ``data.obsm``. By default, use PCA coordinates.

    resolution: ``int``, optional, default: ``1.3``
        Resolution factor. Higher resolution tends to find more clusters with smaller sizes.

    rep_kmeans: ``str``, optional, default: ``"diffmap"``
        The embedding representation on which the KMeans runs. Keyword must exist in ``data.obsm``. By default, use Diffusion Map coordinates. If diffmap is not calculated, use PCA coordinates instead.

    n_clusters: ``int``, optional, default: ``30``
        The number of first level clusters.

    n_clusters2: ``int``, optional, default: ``50``
        The number of second level clusters.

    n_init: ``int``, optional, default: ``10``
        Number of kmeans tries for the first level clustering. Default is set to be the same as scikit-learn Kmeans function.

    random_state: ``int``, optional, default: ``0``
        Random seed for reproducing results.

    class_label: ``str``, optional, default: ``"spectral_louvain_labels"``
        Key name for storing cluster labels in ``data.obs``.

    Returns
    -------
    ``None``

    Update ``data.obs``:
        * ``data.obs[class_label]``: Cluster labels for cells as categorical data.

    Examples
    --------
    >>> pg.spectral_louvain(data)
    """

    try:
        import louvain as louvain_module
    except ImportError:
        print("Need louvain! Try 'pip install louvain-github'.")

    if "X_" + rep_kmeans not in data.obsm.keys():
        logger.warning(
            "{} is not calculated, switch to pca instead.".format(rep_kmeans)
        )
        rep_kmeans = "pca"
        if "X_" + rep_kmeans not in data.obsm.keys():
            raise ValueError("Please run {} first!".format(rep_kmeans))
    if "W_" + rep not in data.uns:
        raise ValueError("Cannot find affinity matrix. Please run neighbors first!")

    labels = partition_cells_by_kmeans(
        data.obsm[rep_kmeans], n_clusters, n_clusters2, n_init, random_state,
    )

    W = data.uns["W_" + rep]

    G = construct_graph(W)
    partition_type = louvain_module.RBConfigurationVertexPartition
    partition = partition_type(
        G, resolution_parameter=resolution, weights="weight", initial_membership=labels
    )
    partition_agg = partition.aggregate_partition()

    optimiser = louvain_module.Optimiser()
    optimiser.set_rng_seed(random_state)
    diff = optimiser.optimise_partition(partition_agg)
    partition.from_coarse_partition(partition_agg)

    labels = np.array([str(x + 1) for x in partition.membership])
    categories = natsorted(np.unique(labels))
    data.obs[class_label] = pd.Categorical(values=labels, categories=categories)

    n_clusters = data.obs[class_label].cat.categories.size
    logger.info(f"Spectral Louvain clustering is done. Get {n_clusters} clusters.")


@timer(logger=logger)
def spectral_leiden(
    data: MultimodalData,
    rep: str = "pca",
    resolution: float = 1.3,
    rep_kmeans: str = "diffmap",
    n_clusters: int = 30,
    n_clusters2: int = 50,
    n_init: int = 10,
    random_state: int = 0,
    class_label: str = "spectral_leiden_labels",
) -> None:
    """Cluster the data using Spectral Leiden algorithm. [Li20]_

    Parameters
    ----------
    data: ``pegasusio.MultimodalData``
        Annotated data matrix with rows for cells and columns for genes.

    rep: ``str``, optional, default: ``"pca"``
        The embedding representation used for clustering. Keyword ``'X_' + rep`` must exist in ``data.obsm``. By default, use PCA coordinates.

    resolution: ``int``, optional, default: ``1.3``
        Resolution factor. Higher resolution tends to find more clusters.

    rep_kmeans: ``str``, optional, default: ``"diffmap"``
        The embedding representation on which the KMeans runs. Keyword must exist in ``data.obsm``. By default, use Diffusion Map coordinates. If diffmap is not calculated, use PCA coordinates instead.

    n_clusters: ``int``, optional, default: ``30``
        The number of first level clusters.

    n_clusters2: ``int``, optional, default: ``50``
        The number of second level clusters.

    n_init: ``int``, optional, default: ``10``
        Number of kmeans tries for the first level clustering. Default is set to be the same as scikit-learn Kmeans function.

    random_state: ``int``, optional, default: ``0``
        Random seed for reproducing results.

    class_label: ``str``, optional, default: ``"spectral_leiden_labels"``
        Key name for storing cluster labels in ``data.obs``.

    Returns
    -------
    ``None``

    Update ``data.obs``:
        * ``data.obs[class_label]``: Cluster labels for cells as categorical data.

    Examples
    --------
    >>> pg.spectral_leiden(data)
    """

    try:
        import leidenalg
    except ImportError:
        print("Need leidenalg! Try 'pip install leidenalg'.")

    if "X_" + rep_kmeans not in data.obsm.keys():
        logger.warning(
            "{} is not calculated, switch to pca instead.".format(rep_kmeans)
        )
        rep_kmeans = "pca"
        if "X_" + rep_kmeans not in data.obsm.keys():
            raise ValueError("Please run {} first!".format(rep_kmeans))
    if "W_" + rep not in data.uns:
        raise ValueError("Cannot find affinity matrix. Please run neighbors first!")

    labels = partition_cells_by_kmeans(
        data.obsm[rep_kmeans], n_clusters, n_clusters2, n_init, random_state,
    )

    W = data.uns["W_" + rep]

    G = construct_graph(W)
    partition_type = leidenalg.RBConfigurationVertexPartition
    partition = partition_type(
        G, resolution_parameter=resolution, weights="weight", initial_membership=labels
    )
    partition_agg = partition.aggregate_partition()

    optimiser = leidenalg.Optimiser()
    optimiser.set_rng_seed(random_state)
    diff = optimiser.optimise_partition(partition_agg, -1)
    partition.from_coarse_partition(partition_agg)

    labels = np.array([str(x + 1) for x in partition.membership])
    categories = natsorted(np.unique(labels))
    data.obs[class_label] = pd.Categorical(values=labels, categories=categories)

    n_clusters = data.obs[class_label].cat.categories.size
    logger.info(f"Spectral Leiden clustering is done. Get {n_clusters} clusters.")


def cluster(
    data: MultimodalData,
    algo: str = "louvain",
    rep: str = "pca",
    resolution: int = 1.3,
    random_state: int = 0,
    class_label: str = None,
    n_iter: int = -1,
    rep_kmeans: str = "diffmap",
    n_clusters: int = 30,
    n_clusters2: int = 50,
    n_init: int = 10,
) -> None:
    """Cluster the data using the chosen algorithm.

    Candidates are *louvain*, *leiden*, *spectral_louvain* and *spectral_leiden*.
    If data have < 1000 cells and there are clusters with sizes of 1, resolution is automatically reduced until no cluster of size 1 appears.

    Parameters
    ----------
    data: ``pegasusio.MultimodalData``
        Annotated data matrix with rows for cells and columns for genes.

    algo: ``str``, optional, default: ``"louvain"``
        Which clustering algorithm to use. Choices are louvain, leiden, spectral_louvain, spectral_leiden

    rep: ``str``, optional, default: ``"pca"``
        The embedding representation used for clustering. Keyword ``'X_' + rep`` must exist in ``data.obsm``. By default, use PCA coordinates.

    resolution: ``int``, optional, default: ``1.3``
        Resolution factor. Higher resolution tends to find more clusters.

    random_state: ``int``, optional, default: ``0``
        Random seed for reproducing results.

    class_label: ``str``, optional, default: None
        Key name for storing cluster labels in ``data.obs``. If None, use 'algo_labels'.

    n_iter: ``int``, optional, default: ``-1``
        Number of iterations that Leiden algorithm runs. If ``-1``, run the algorithm until reaching its optimal clustering.

    rep_kmeans: ``str``, optional, default: ``"diffmap"``
        The embedding representation on which the KMeans runs. Keyword must exist in ``data.obsm``. By default, use Diffusion Map coordinates. If diffmap is not calculated, use PCA coordinates instead.

    n_clusters: ``int``, optional, default: ``30``
        The number of first level clusters.

    n_clusters2: ``int``, optional, default: ``50``
        The number of second level clusters.

    n_init: ``int``, optional, default: ``10``
        Number of kmeans tries for the first level clustering. Default is set to be the same as scikit-learn Kmeans function.

    Returns
    -------
    ``None``

    Update ``data.obs``:
        * ``data.obs[class_label]``: Cluster labels of cells as categorical data.

    Examples
    --------
    >>> pg.cluster(data, algo = 'leiden')
    """

    if algo not in {"louvain", "leiden", "spectral_louvain", "spectral_leiden"}:
        raise ValueError("Unknown clustering algorithm {}.".format(algo))

    if class_label is None:
        class_label = algo + "_labels"

    kwargs = {
        "data": data,
        "rep": rep,
        "resolution": resolution,
        "random_state": random_state,
        "class_label": class_label,
    }
    if algo == "leiden":
        kwargs["n_iter"] = n_iter
    if algo in ["spectral_louvain", "spectral_leiden"]:
        kwargs.update(
            {
                "rep_kmeans": rep_kmeans,
                "n_clusters": n_clusters,
                "n_clusters2": n_clusters2,
                "n_init": n_init,
            }
        )

    cluster_func = globals()[algo]

    cluster_func(**kwargs)  # clustering
    if data.shape[0] < 100000 and data.obs[class_label].value_counts().min() == 1:
        new_resol = resolution
        while new_resol > 0.0:
            new_resol -= 0.1
            kwargs["resolution"] = new_resol
            cluster_func(**kwargs)
            if data.obs[class_label].value_counts().min() > 1:
                break
        logger.warning(
            "Reduced resolution from {:.2f} to {:.2f} to avoid clusters of size 1.".format(
                resolution, new_resol
            )
        )
